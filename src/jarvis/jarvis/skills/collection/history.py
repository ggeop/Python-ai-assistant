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

from jarvis.skills.skill import AssistantSkill
from jarvis.utils.mongoDB import db

header = """
-----------------------------------------------------------------------------------------------
- History                                                                                     -
-----------------------------------------------------------------------------------------------
* Note: The default limit is 3. Change the limit by adding a number e.g show me user history 10.

"""

response_base = """
* User Transcript: {0}
* Response: {1}
* Executed Skill: {2}
-----------------------------------------------------------------------------------------------"""


class HistorySkills(AssistantSkill):
    default_limit = 3

    @classmethod
    def show_history_log(cls, voice_transcript, skill):
        """
        This method cls.consoles user commands history & assistant responses.

        """

        limit = cls._extract_history_limit(voice_transcript, skill)
        limit = limit if limit else cls.default_limit
        documents = db.get_documents(collection='history', limit=limit)
        response = cls._create_response(documents)
        cls.console(response)

    @classmethod
    def _create_response(cls, documents):
        response = ''
        try:
            for document in documents:
                response += response_base.format(document.get('user_transcript', '--'),
                                                 document.get('response', '--'),
                                                 document.get('executed_skill').get('skill').get('name') if
                                                 document.get('executed_skill') else '--'
                                                 )
        except Exception as e:
            cls.console(error_log=e)
        finally:
            from jarvis.utils import input, console
            return header + response

    @classmethod
    def _extract_history_limit(cls, voice_transcript, skill):
        tags = cls.extract_tags(voice_transcript, skill['tags'])
        only_number_regex = '([0-9]+$)'
        for tag in tags:
            reg_ex = re.search(tag + ' ' + only_number_regex, voice_transcript)
            if reg_ex:
                limit = int(reg_ex.group(1))
                return limit
