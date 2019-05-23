class Processor:
    def __init__(self):
        self.command_manager = CommandManager()

    def run(self):
        start_up()
        while True:
            self._process()
            self.command_manager.shutdown_check()

    def _process(self):
        # Check if the assistant is waked up
        if self.command_manager.wake_up_check():

            # Record user voice and create a voice transcipt
            self.command_manager._get_voice_transcript()

            # Extract commands and update the commands (state of command manager)
            self.command_manager._get_user_commands()

            # If there are commands execute them
            if self.command_manager.commands:
                self._execute()
