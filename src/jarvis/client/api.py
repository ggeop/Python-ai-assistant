from enum import Enum

class Status_code(Enum):
    Success = 200
    Server_Error = 500
    Client_Error = 400


class api_manager:
    def __init__(self) -> None:
        pass
    
    def post_user_input(transcript: str) -> Status_code:
        pass