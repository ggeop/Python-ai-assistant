from jarvis.command_manager import CommandManager
from jarvis.assistant_utils import start_up


def main():
    command_controller = CommandManager()
    start_up()
    while True:
        if command_controller.wake_up_check():
            command_controller.run()
        command_controller.shutdown_check()


if __name__ == '__main__':
    main()
