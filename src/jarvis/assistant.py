from jarvis.action_controller import ActionController
from jarvis.command_controller import CommandController
from jarvis.assistant_utils import assistant_response


def main():
    assistant_response("Hi!!")
    while True:
        words = CommandController.get_words()
        if ActionController.wake_up(words):
            assistant_response('What do you want to do for you sir?')
            commands = CommandController.run(words)

        ActionController.shutdown(words)


if __name__ == '__main__':
    main()
