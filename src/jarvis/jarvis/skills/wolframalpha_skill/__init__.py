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

import logging
import wolframalpha


from jarvis.settings import WOLFRAMALPHA_API


def call_wolframalpha(voice_transcript):
    """
    Make a request in wolfram Alpha API and prints the response.
    """
    client = wolframalpha.Client(WOLFRAMALPHA_API['key'])
    if voice_transcript:
        try:
            if WOLFRAMALPHA_API['key']:
                res = client.query(voice_transcript)
                print(next(res.results).text)
                logging.debug('Successful response from Wolframalpha')
            else:
                print("WolframAlpha API is not working.\n"
                                   "You can get an API key from: https://developer.wolframalpha.com/portal/myapps/ ")
        except Exception as e:
            logging.debug('There is not answer with wolframalpha with error: {0}'.format(e))
            print('Sorry, but I can not understand what do you want')
