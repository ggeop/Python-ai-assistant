import engines
from api import api_manager

class Client:
    def __init__(self, console_manager) -> None:
        self.console_manager = console_manager
        self.api_manger = api_manager()
    
    def run() -> None:
        """
         Assistant starting point.

        - STEP 1: Get user input based on the input mode (voice or text)
        - STEP 2: Send the user input to the api
        - STEP 3: Get api response and either execute a local skill or give the user a respone

        """
        transcript = engines.input_engine.recognize_input()
        self.api_manger.post_user_input(transcript)
