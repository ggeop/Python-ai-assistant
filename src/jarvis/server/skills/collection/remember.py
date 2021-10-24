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


from jarvis.skills.skill import AssistantSkill
from jarvis.utils.mongoDB import db
from jarvis.utils import input

header = """
-----------------------------------------------------------------------------------------------
I would like to learn, tell me the right answer!
-----------------------------------------------------------------------------------------------
* Note: Create new skill! Write your question and the appropriate answer.
\n
"""


class RememberSkills(AssistantSkill):

    @classmethod
    def remember(cls, **kwargs):
        cls.console(header)
        continue_add = True
        while continue_add:
            cls.console(text='Question: ')
            tags = cls.user_input()
            cls.console(text='Suggested Response: ')
            response = cls.user_input()
            new_skill = {'name': 'learned_skill',
                         'enable': True,
                         'func': cls.tell_response.__name__,
                         'response': response,
                         'tags': tags,
                         },

            cls.response('Add more? ', refresh_console=False)
            continue_add = input.check_input_to_continue()
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
            cls.response('Are you sure to remove learned skills? ', refresh_console=False)
            user_answer = input.check_input_to_continue()
            if user_answer:
                db.drop_collection(collection='learned_skills')
                cls.response("Perfect I have deleted them all")
