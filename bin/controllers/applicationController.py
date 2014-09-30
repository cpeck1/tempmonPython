def main():
    # Setup
    contexts = {Context(1, "Chest Freezer", "Temperature", -80.0, 15)}
    

    # Loop
    while True:
        # refresh any alarms that need it
        refresh = {c for c in contexts 
                   if c.active_alarm is not None 
                   and c.active_alarm.requires_refresh(c.read_frequency)}
        for c in refresh: c.active_alarm.refresh()

        # prepare any unprepared transmitter
        needs_prep = {c for c in contexts 
                      where not c.transmitter_open()}
        for c in needs_prep: c.transmitter.open()
        
        # any transmitter that is still not ready must be reported as an error
        with_transmitter_errors = {c for c in contexts
                                   where not c.transmitter_open()}
        for c in with_transmitter_errors: c.activate_alarm(c.transmitter)

        # read the contexts with transmitters that are not defunct
        to_read = List(contexts - with_transmitter_errors)
        readings = [c.transmitter.read() for c in contexts]

        # have each context process its own reading
        for (c, r) in zip(to_read, readings):
            c.process_reading(r)
