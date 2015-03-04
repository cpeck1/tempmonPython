class MessageWriter:
    def write_error_notification(context, error):
        message = "An error occurred in the following context: \n\t"
        message = message + str(context).replace('\n', '\n\t')

        message = message + "\n"
        message = message + "The following error was produced: \n\t"
        message = message + str(error).replace('\n', '\n\t')

        return message

    def write_alarm_notification(context, alarm, ended=False):
        message = "An alarm was triggered in the following context: \n\t"
        message = message + str(context).replace('\n', '\n\t')
        message = message + "\n"
        
        if not ended:
            message = message + "The following alarm was triggered: "
        else:
            message = message + "The following alarm has ended: "

        message = message + str(alarm).replace('\n', '\n\t')

        message = message + "\n"
        message = message + "The alarm was triggered at: "
        message = message + str(alarm.start_time)
        if ended:
            message + "\n"
            message + "The alarm ended at: " + str(alarm.end_time)
        
        return message
