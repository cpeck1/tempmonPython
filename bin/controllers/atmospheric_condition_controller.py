from ..models.alarm import Alarm

class AtmosphericConditionController:
    def __init__(self, conditions):
        self.atmospheric_conditions = conditions

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
                    condition.channel = channel
                    channels.remove(channel)
                    break
            if condition.channel is None:
                no_channels.append(condition)
        return no_channels

    def gather_readings(self):
        alarms = [] # alarms that are starting as well as ending
        for ac in self.atmospheric_conditions:
            if ac.channel is None: continue

            reading = ac.read_channel()
            if ac.expectation.violated_by(reading):
                if ac.alarm_active():
                    if ac.record_due(): 
                        ac.readings.append(reading)
                else:
                    ac.readings.append(reading)
                    alarm = Alarm(
                        reading=reading,
                        expectation=ac.expectation
                    )
                ac.alarms.append(alarm)
                alarms.append(alarm)
            elif ac.alarm_active(): 
                ac.readings.append(reading)

                alarm = ac.most_recent_alarm()
                alarm.end()
                alarms.append(alarm)
            else: # reading within safe range and no alarm active
                if ac.record_due():
                    ac.readings.append(reading)
        return alarms
