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


from jarvis.skills.assistant_skill import AssistantSkill
from jarvis.utils.mongoDB import db
from jarvis.utils import user_input

header = """
-----------------------------------------------------------------------------------------------
I would like to learn, tell me the right answer!
-----------------------------------------------------------------------------------------------
* Note: Create new skill! Write your question and the appropriate answer.
\n
"""


class LearnSkills(AssistantSkill):

    @classmethod
    def learn(cls, **kwargs):
        cls.console(header)
        continue_add = 'y'
        while continue_add == 'y':
            # TODO: Add also speech input based on assistant mode.
            tags = input('Question: ')
            response = input('Suggested Response: ')
            new_skill = {'name': 'learned_skill',
                         'enable': True,
                         'func': cls.tell_response.__name__,
                         'response': response,
                         'tags': tags,
                         },

            continue_add = input('Continue add skills (y/n): ').lower()
            db.insert_many_documents(collection='learned_skills', documents=new_skill)

    @classmethod
    def tell_response(cls, **kwargs):
        cls.response(kwargs.get('skill').get('response'))

    @classmethod
    def clear_learned_skills(cls, **kwargs):
        if db.is_collection_empty(collection='learned_skills'):
            cls.response("I can't find learned skills in my database")
        else:
            cls.response('I found learned skills..')
            user_input.check_input_to_continue('Are you sure to remove learned skills')
            user_answer = input('Are you sure to remove learned skills (y/n): ').lower()
            if user_answer:
                db.drop_collection(collection='learned_skills')
                cls.response("Perfect I have deleted them all")
