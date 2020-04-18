# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def validate_digits_input(message):
    while True:
        try:
            user_input = int(input(message + ' '))
        except ValueError:
            print("Please give a number ONLY e.g 100, 300")
            continue
        else:
            break
    return user_input


def check_input_to_continue(message):
    positive_answers = ['yes', 'y', 'sure', 'yeah']
    return input(message + ' (y/n): ').lower() in positive_answers


def validate_input_with_choices(message, available_choices):
    user_input = input(message)
    while not user_input in available_choices:
        print('Please select on of the values: {0}'.format(available_choices))
        user_input = input('Set input mode: ')
    return user_input

