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

from typing import Optional
from fastapi import FastAPI
from server.core.nlp import ResponseCreator
from server.settings import SKILL_ANALYZER
from server.skills.registry import BASIC_SKILLS
from server.skills.analyzer import SkillAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from bson import ObjectId
from server.utils.mongoDB import db

from server import settings
class Processor:
    def __init__(self):
        self.response_creator = ResponseCreator()
        self.skill_analyzer = SkillAnalyzer(
            weight_measure=TfidfVectorizer,
            similarity_measure=cosine_similarity,
            args=settings.SKILL_ANALYZER.get('args'),
            sensitivity=settings.SKILL_ANALYZER.get('sensitivity'),
        )
        self.skill = {}
        self.response = {}
    def all_skills(self):
        return len(BASIC_SKILLS)
    def extract_command(self, transcript):
        skill = self.skill_analyzer.extract(transcript)
        print(skill)
        if skill:
            return {'voice_transcript': transcript, 'skill': skill, 'response' :self.response_creator.create_positive_response(transcript)}

        else:
            return {'voice_transcript': transcript,
                                'skill': {'name': WolframSkills.call_wolframalpha.__name__},
                                'response': self.response_creator.create_negative_response(transcript)
                                }
    def _execute_skill(self, skill):
        if skill:
            skill_func_name = skill.get('skill').get('func')
            try:
                ActivationSkills.enable_assistant()
                skill_func_name = skill.get('skill').get('func')
                skill_func = skill_objects[skill_func_name]
                skill_func(**skill)
            except Exception as e:
                return "Failed to execute skill {0} with message: {1}".format(skill_func_name, e)
    def query_wolfram(self, query):
        WolframSkills.call_wolframalpha(query)
    def write_to_db(self,transcript):
        record = {'user_transcript': transcript,
                  'response': self.response if self.response else '--',
                  'executed_skill': self.skill  if self.skill else '--'
                  }

        db.insert_many_documents('history', [record])

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = FastAPI()
processor = Processor()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/commands")
def list_skills():
    return {'skills':processor.all_skills()}

@app.post("/commands")
def extract_skill(transcript: str):
    skill = processor.extract_command(transcript)
    return JSONEncoder().encode(skill)
@app.get("/execute/{skill_id}")
def extract_skill(skill_id: str):
    skill= db.findOne('control_skills', skill_id)
    print(skill_id)
    response = processor._execute_skill(skill)
    return response