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

import re
import time

from jarvis.skills.skill import AssistantSkill


class WordSkills(AssistantSkill):
    
    @classmethod
    def spell_a_word(cls, voice_transcript, skill, **kwargs):
        """
        Spell a words letter by letter.
        :param voice_transcript: string (e.g 'spell word animal')
        :param skill: dict (e.g
        """
        tags = cls.extract_tags(voice_transcript, skill['tags'])
        for tag in tags:
            reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
            try:
                if reg_ex:
                    search_text = reg_ex.group(1)
                    for letter in search_text:
                        cls.response(letter)
                        time.sleep(2)
            except Exception as e:
                cls.console(error_log=e)
                cls.response("I can't spell the word")
