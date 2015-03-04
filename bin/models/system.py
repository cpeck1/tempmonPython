# MOVE THIS WHOLE DAMN THING TO A CONTROLLER application_controller.py!
import copy
from datetime import datetime, timedelta

from sqlalchemy import *
from models.base import Base
from sqlalchemy.orm import relationship

from models.environment import Environment
from models.atmospheric_condition import AtmosphericCondition
from models.expectation import Expectation
from models.reading import Reading
from models.alarm import Alarm
from models.admin import Admin
from models.transmitter import Transmitter
from models.channel import Channel

from services.message_writer import MessageWriter

read_retry_limit = 5

# bunch of fake functions to get the structure right
def load_database():
    pass

def load_environments_from_database():
    e = Environment()
    exp = Expectation(units='Celsius', low=-86, high=-80)
    ac = AtmosphericCondition(
        type="Temperature", 
        recording_frequency=timedelta(seconds=5),
        expectation=exp
    )

    e.atmospheric_conditions.append(ac)

    return [e]

def load_transmitters_from_usb_ports():
    t = Transmitter()
    t.channels.append(Channel())
    return [t]

def load_admins_from_database():
    a = Admin()

    return [a]

class System(Base):
    __tablename__ = "system"
    id = Column(Integer, primary_key=True)

    environments = relationship("Environment", backref='system', 
                                cascade="all, delete, delete-orphan")
    transmitters = relationship("Transmitter", backref='system',
                                cascade="all, delete, delete-orphan")
    admins = relationship("Admin", backref='system',
                          cascade="all, delete, delete-orphan")

    # def __init__(self, id):
    #     self.id = id

    #     self.database_url = None
    #     self.database = None

    #     self.environments = {}
    #     self.transmitters = {}
    #     self.admins = {}

    def __repr__(self):
        return "System(id={!r}, environments={!r}, transmitters={!r}, admins={!r})".format(self.id, self.environments, self.transmitters, self.admins)

    def __str__(self):
        # Prettified string of the system
        s = "System: \n\t"
        s = s + "id: {!r} \n\t".format(self.id)
        
        s = s + "environments: \n\t\t"
        for e in self.environments:
            s = s + str(e).replace("\n", "\n\t\t")
            s = s + "\n\t\t"

        s = s + "\n\ttransmitters: \n\t\t"
        for t in self.transmitters:
            s = s + str(t).replace("\n", "\n\t\t")
            s = s + "\n\t\t"
            
        s = s + "\n\tadmins: \n\t\t"
        for a in self.admins:
            s = s + str(a).replace("\n", "\n\t\t")
            s = s + "\n\t\t"

        return s

    def run(self):
        load_env_flag = 1
        load_trans_flag = 1
        load_admin_flag = 1
        
        functional_environments = []

        while True:
            if load_env_flag: # load environments flag
                # TODO implement this function
                self.environments = (
                    load_environments_from_database()
                )
            if load_trans_flag: # load transmitters flag
                # set when a USB device is plugged into or removed from
                # the system

                # includes things like opening the transmitter and all  
                # of its channels and assigning read method?

                # TODO implement this function
                self.transmitters = load_transmitters_from_usb_ports()
            if load_admin_flag: # yeah
                # TODO implement this function
                self.admins = load_admins_from_database()
            if load_env_flag or load_trans_flag: 
                environment_errors = set()

                # don't want the transmitters disappearing permanently 
                # but want to be able to discard them while assigning 
                # them to atmospheric conditions so that no duplicates
                # are assigned; hence, copy
                for e in self.environments:
                    for ac in e.atmospheric_conditions:
                        ch = ac.claim_transmitter_channel(
                            transmitter_set=self.transmitters
                        )
                        if ch is None:
                            # append the tuple (e, ac) so that ac can be
                            # cited as the source of the error for 
                            # environment e
                            environment_errors.add((e, ac))
                        else:
                            functional_environments.append(e)
                for (e, ac) in environment_errors:
                    for a in self.admins:
                        a.report(
                            message=MessageWriter.write_error_notification(
                                context=self, 
                                error=("No transmitter channel found for "+
                                       "atmospheric condition: \n"+ str(ac))
                                )
                        )

                load_env_flag = load_trans_flag = load_admin_flag = 0
                # end load block

            for e in functional_environments:
                for ac in e.atmospheric_conditions:
                    reading = None
                    attempt = 0
                    while reading is None and attempt < read_retry_limit:
                        reading = ac.request_channel_read()
                        attempt += 1
                    
                    if reading is None:
                        for a in self.admins:
                            a.report(
                                message=MessageWriter.write_error_notification(
                                    context=self,
                                    error=("Transmitter channel did not " + 
                                         "return readings for atmospheric " +
                                         "condition: \n" + str(ac))
                                    )
                            )
                    else: # got a reading from the transmitter channel
                        if ac.expectation.violated_by(reading=reading):
                            if e.alarm_going_off(atmospheric_condition=ac):
                                if e.record_due(atmospheric_condition=ac):
                                    e.record_reading(
                                        atmospheric_condition=ac, 
                                        reading=reading
                                    )
                            else:
                                alarm = e.activate_alarm(
                                    atmospheric_condition=ac, 
                                    cause=reading
                                )
                                for a in self.admins:
                                    a.report(
                                        MessageWriter.write_alarm_notification(
                                            context=e,
                                            alarm=alarm
                                        )
                                    )
                                e.record_reading(
                                    atmospheric_condition=ac, 
                                    reading=reading
                                )
                        else: # reading did NOT violate expectations
                            # any time we get a reading that would end
                            # an ongoing alarm we must record it
                            if e.alarm_going_off(atmospheric_condition=ac):
                                alarm = e.end_alarm(atmospheric_condition=ac)
                                for a in self.admins:
                                    a.report(
                                        MessageWriter.write_alarm_notification(
                                            context=e,
                                            alarm=alarm,
                                            ended=True
                                        )
                                    )
                                e.record_reading(
                                    atmospheric_condition=ac, 
                                    reading=reading
                                )
                            elif e.record_due(atmospheric_condition=ac): 
                                e.record_reading(
                                    atmospheric_condition=ac, 
                                    reading=reading
                                )
