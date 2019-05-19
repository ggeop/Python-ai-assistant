from jarvis.command_manager import CommandController
from jarvis.assistant_utils import start_up


def main():
    command_controller = CommandController()
    start_up()
    while True:
        if command_controller.wake_up_check():
            command_controller.run()
        command_controller.shutdown_check()


if __name__ == '__main__':
    main()
