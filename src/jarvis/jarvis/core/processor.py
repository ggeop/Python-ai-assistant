from jarvis.core.controller import SkillsController
from jarvis.utils.application_utils import start_up
from jarvis.skills.wolframalpha_skill.__init__ import call_wolframalpha


class Processor:
    def __init__(self):
        self.controller = SkillsController()

    def run(self):
        start_up()
        while True:
            self._process()

    def _process(self):
        # Check if the assistant is waked up
        if self.controller.wake_up_check():

            self.controller.get_transcript()
            self.controller.get_skills()

            if self.controller.skills_to_execute:
                self.controller.execute()
            else:
                self.controller.shutdown_check()

                # If there is not an action the assistant make a request in WolframAlpha API
                call_wolframalpha(self.controller.latest_voice_transcript)

        self.controller.shutdown_check()