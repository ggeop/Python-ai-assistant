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

import wolframalpha

from jarvis.settings import WOLFRAMALPHA_API
from jarvis.skills.collection.internet import InternetSkills
from jarvis.skills.skill import AssistantSkill


class WolframSkills(AssistantSkill):
    
    @classmethod
    def call_wolframalpha(cls, voice_transcript, **kwargs):
        """
        Make a request in wolfram Alpha API and prints the response.
        """
        client = wolframalpha.Client(WOLFRAMALPHA_API['key'])
        if voice_transcript:
            try:
                if WOLFRAMALPHA_API['key']:
                    cls.console(info_log='Wolfarm APi call with query message: {0}'.format(voice_transcript))
                    cls.response("Wait a second, I search..")
                    res = client.query(voice_transcript)
                    wolfram_result = next(res.results).text
                    cls.console(debug_log='Successful response from Wolframalpha')
                    cls.response(wolfram_result)
                    return wolfram_result
                else:
                    cls.response("WolframAlpha API is not working.\n"
                          "You can get an API key from: https://developer.wolframalpha.com/portal/myapps/ ")
            except Exception as e:
                if InternetSkills.internet_availability():
                    # If there is an error but the internet connect is good, then the Wolfram API has problem
                    cls.console(error_log='There is no result from Wolfram API with error: {0}'.format(e))
                else:
                    cls.response('Sorry, but I could not find something')
