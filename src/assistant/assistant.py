from assistant.action_controller import ActionController
from assistant.command_controller import CommandController
from assistant.assistant_utils import assistant_response


def main():
    assistant_response("Hi!!")
    while True:
        words = CommandController.get_words()
        if ActionController.wake_up(words):
            assistant_response('What do you want sir?')
            words = CommandController.get_words()

            commands = CommandController.get_commands(words)
            CommandController.execute_commands(commands, words)

        ActionController.shutdown(words)


if __name__ == '__main__':
    main()
