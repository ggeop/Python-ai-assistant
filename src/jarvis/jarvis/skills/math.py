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

from jarvis.skills.assistant_skill import AssistantSkill
from jarvis.utils.mapping import math_symbols_mapping


class MathSkills(AssistantSkill):
    
    @classmethod
    def do_calculations(cls, voice_transcript, **kwargs):
        # ------------------------------------------------
        # Current Limitations
        # ------------------------------------------------
        # * Only basic operators are supported
        # * In the text need spaces to understand the input e.g 3+4 it's not working, but 3 + 4 works!

        math_equation = cls._clear_transcript(voice_transcript)
        try:
            result = str(eval(math_equation))
            cls.response(result)
        except Exception as e:
            logging.error('Failed to eval the equation --> {0} with error message {1}'.format(math_equation, e))

    @classmethod
    def _clear_transcript(cls, transcript):
        cleaned_transcript = ''
        for word in transcript.split():
            if word.isdigit() or word in math_symbols_mapping.values():
                cleaned_transcript += word
            else:
                cleaned_transcript += math_symbols_mapping.get(word, '')
        return cleaned_transcript
