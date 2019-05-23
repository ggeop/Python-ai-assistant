from jarvis.action_controller import ActionController


class Processor:
    def __init__(self):
        self.action_controller = ActionController()

    def run(self):
        start_up()
        while True:
            self._process()
            self.action_controller.shutdown_check()

    def _process(self):
        # Check if the assistant is waked up
        if self.action_controller.wake_up_check():

            # Record user voice and create a voice transcipt
            self.action_controller._get_voice_transcript()

            # Extract actions and update the actions (state of action controller)
            self.action_controller._get_user_actions()

            # If there are actions execute them
            if self.action_controller.actions:
                self._execute()
