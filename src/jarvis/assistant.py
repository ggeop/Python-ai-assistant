from jarvis.action_controller import ActionController
from jarvis.command_controller import CommandController
from jarvis.assistant_utils import assistant_response


def main():
    command_controller = CommandController()
    assistant_response("Hi!!")
    while True:
        if command_controller.wake_up():
            commands = command_controller.run()
        command_controller.shutdown()


if __name__ == '__main__':
    main()
