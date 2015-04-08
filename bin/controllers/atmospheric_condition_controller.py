import logging
from bin.models.alarm import Alarm
from bin.models.reading import Reading

logger = logging.getLogger("monitoring_application")

class AtmosphericConditionController:
    def __init__(self, dbsession, conditions):
        self.atmospheric_conditions = conditions
        self.dbsession = dbsession

    def assign_channels(self, channels):
        no_channels = []
        for condition in self.atmospheric_conditions:
            for channel in channels:
                match_found = (
                    (condition.channel_bus == channel.bus) and
                    (condition.channel_address == channel.address) and
                    (condition.channel_number == channel.channel_number)
                )
                if match_found:
                    logger.info(repr(condition)+" matched "+repr(channel))
                    condition.channel = channel
                    channels.remove(channel)
                    break

            if condition.channel is None:
                no_channels.append(condition)
                logger.error("No channel match found for "+repr(condition))
        return no_channels

    def gather_readings(self):
        alarms = [] # alarms that are starting as well as ending
        for ac in self.atmospheric_conditions:
            if ac.channel is None: 
                continue
            
            reading = ac.read_channel()
            if reading is None:
                logger.error(repr(ac.channel)+" failed to gather reading.")
                continue

            logger.debug(repr(reading)+" gathered for "+repr(ac))
            if ac.expectation.violated_by(reading):
                logger.debug(
                    repr(reading)+" violated expectation "+repr(ac.expectation)
                )
                if ac.alarm_active():
                    if ac.record_due(): 
                        ac.readings.append(
                            Reading(
                                units=reading.units, 
                                value=reading.value, 
                                time=reading.time
                            )
                        )
                        self.dbsession.add(ac)
                else: # alarm not active, reading activates alarm
                    ac.readings.append(
                        Reading(
                            units=reading.units, 
                            value=reading.value, 
                            time=reading.time
                        )
                    )
                    ac.alarms.append(
                        Alarm(
                            reading=ac.most_recent_reading(),
                            expectation=ac.expectation
                        )
                    )
                    logger.info("Started alarm: "+repr(ac.most_recent_alarm()))
                    alarms.append(ac.most_recent_alarm())
                    self.dbsession.add(ac)

            elif ac.alarm_active(): # reading in safe range ends alarm
                ac.readings.append(
                    Reading(
                        units=reading.units, 
                        value=reading.value, 
                        time=reading.time
                    )
                )
                alarm = ac.most_recent_alarm()
                alarm.end()
                logger.debug("Alarm "+repr(alarm)+" ended by reading") 
                alarms.append(alarm)
                
                self.dbsession.add(ac)

            else: # reading within safe range and no alarm active
                if ac.record_due():
                    logger.debug("Record due, recording reading...")
                    ac.readings.append(
                        Reading(
                            units=reading.units, 
                            value=reading.value, 
                            time=reading.time
                        )
                    )
                    self.dbsession.add(ac)
        self.dbsession.commit()
        return alarms
