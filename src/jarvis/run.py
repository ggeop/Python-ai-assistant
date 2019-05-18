from jarvis.command_manager import CommandController


def main():
    command_controller = CommandController()
    while True:
        if command_controller.wake_up_check():
            command_controller.run()
        command_controller.shutdown_check()


if __name__ == '__main__':
    main()
