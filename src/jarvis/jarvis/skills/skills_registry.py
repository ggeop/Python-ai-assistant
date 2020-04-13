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

from jarvis.skills.assistant_activation import ActivationSkills
from jarvis.skills.assistant_info import AssistantInfoSkills
from jarvis.skills.datetime import DatetimeSkills
from jarvis.skills.browser import BrowserSkills
from jarvis.skills.util_skills import UtilSkills
from jarvis.skills.internet import InternetSkills
from jarvis.skills.libreoffice_suite import LibreofficeSkills
from jarvis.skills.linux_app import LinuxAppSkills
from jarvis.skills.location import LocationSkill
from jarvis.skills.reminder import ReminderSkill
from jarvis.skills.system_health import SystemHealthSkills
from jarvis.skills.weather import WeatherSkills
from jarvis.skills.text import WordSkills
from jarvis.skills.history import HistorySkills
from jarvis.skills.learn import Learn
from jarvis.settings import GENERAL_SETTINGS
from jarvis.utils.mongoDB import db

# All available assistant skills
# Keys description:
#    - 'enable': boolean (With True are the enabled skills)
#    - 'func': The skill method in Skills
#    - 'tags': The available triggering tags
#    - 'description': skill description

CONTROL_SKILLS = [
    {'name': 'enable_assistant',
     'func': ActivationSkills.enable_assistant,
     'tags': 'start, hi, hello, ' + GENERAL_SETTINGS.get('assistant_name')
     },

    {'name': 'disable_assistant',
     'func': ActivationSkills.disable_assistant,
     'tags': 'bye, shut down, exit, termination'
     }
]

BASIC_SKILLS = [
    {'name': 'assistant_greeting',
     'enable': True,
     'func': ActivationSkills.assistant_greeting,
     'tags': 'good morning, good afternoon, good evening',
     'description': 'Greeting the assistant and he will greeting back e.x good morning Jarvis'
     },

    {'name': 'open_site_in_browser',
     'enable': True,
     'func': BrowserSkills.open_website_in_browser,
     'tags': 'open',
     'description': 'Ask me to "open" a domain in the browser e.x open facebook'
     },

    {'name': 'tell_daily_news',
     'enable': True,
     'func': BrowserSkills.tell_me_today_news,
     'tags': 'news, today news',
     'description': 'Ask me to tell the daily news e.x "Tell me the news today"'
     },

    {'name': 'tell_time',
     'enable': True,
     'func': DatetimeSkills.tell_the_time,
     'tags': 'time, hour',
     'description': 'Ask me for the current "time"'
     },

    {'name': 'tell_date',
     'enable': True,
     'func': DatetimeSkills.tell_the_date,
     'tags': 'date',
     'description': 'Ask me for the current "date"'
     },

    {'name': 'tell_about',
     'enable': True,
     'func': BrowserSkills.tell_me_about,
     'tags': 'about, what is',
     'description': 'Ask me "about" something, e.g. tell me about google, what is google'
     },
    {'name': 'speech_interruption',
     'enable': True,
     'func': UtilSkills.speech_interruption,
     'tags': 'stop',
     'description': 'Tell "stop", to interrupt assistant speech'
     },

    {'name': 'assistant_help',
     'enable': True,
     'func': AssistantInfoSkills.assistant_help,
     'tags': 'help',
     'description': 'Ask me for "help", e.g. Jarvis help me'
     },

    {'name': 'tells_the_weather',
     'enable': True,
     'func': WeatherSkills.tell_the_weather,
     'tags': 'weather, temperature, weather prediction',
     'description': 'Ask for the "weather in" somewhere, e.g. weather in London'
     },

    {'name': 'assistant_check',
     'enable': True,
     'func': AssistantInfoSkills.assistant_check,
     'tags': 'hear, hey jarvis, are you there',
     'description': 'Ask me if I "hear" you, e.g. Jarvis "can you hear" me?'
     },

    {'name': 'libreoffice_calc',
     'enable': True,
     'func': LibreofficeSkills.open_libreoffice_calc,
     'tags': 'calc, excel',
     'description': 'Ask me to "open writer", e.g. Jarvis "can you open calc"?'
     },

    {'name': 'open_libreoffice_writer',
     'enable': True,
     'func': LibreofficeSkills.open_libreoffice_writer,
     'tags': 'writer, word',
     'description': 'Ask me to "open writer", e.g. Jarvis "can you open writer"?'
     },

    {'name': 'open_libreoffice_impress',
     'enable': True,
     'func': LibreofficeSkills.open_libreoffice_impress,
     'tags': 'impress, power point',
     'description': 'Ask me to "open impress", e.g. Jarvis "can you open impress"?'
     },

    {'name': 'tell_memory_consumption',
     'enable': True,
     'func': SystemHealthSkills.tell_memory_consumption,
     'tags': 'ram, ram usage, memory, memory consumption',
     'description': 'Ask for the memory consumption, '
                    'e.g. Jarvis how much "memory" are you using?'
     },

    {'name': 'open_in_youtube',
     'enable': True,
     'func': BrowserSkills.open_in_youtube,
     'tags': 'open in youtube, find in youtube, play in youtube',
     'description': 'Ask for the memory consumption, e.g. Jarvis how much "memory" are you using?'
     },

    {'name': 'run_speedtest',
     'enable': True,
     'func': InternetSkills.run_speedtest,
     'tags': 'speedtest, internet speed, ping',
     'description': 'Ask for internet speedtest, e.g. Jarvis tell_the_skills me the "internet speed"?'
     },

    {'name': 'internet_availability',
     'enable': True,
     'func': InternetSkills.internet_availability,
     'tags': 'internet conection, internet',
     'description': 'Ask for "internet connection", e.g. "Jarvis do we have internet"?'
     },

    {'name': 'spell_a_word',
     'enable': True,
     'func': WordSkills.spell_a_word,
     'tags': 'spell, spell the word',
     'description': 'Ask to spell a word, e.g. Jarvis can you spell the word "animal"?'
     },

    {'name': 'create_reminder',
     'enable': True,
     'func': ReminderSkill.create_reminder,
     'tags': 'reminder, remind me',
     'description': 'Ask to remind you something e.g. "Jarvis create a 5 minute reminder"?'
     },

    {'name': 'tell_the_skills',
     'enable': True,
     'func': AssistantInfoSkills.tell_the_skills,
     'tags': 'skills, your skills, what are your skills',
     'description': 'Ask to tell you what he can do e.g. "Jarvis what can you do"?'
     },

    {'name': 'take_a_note',
     'enable': True,
     'func': LinuxAppSkills.open_note_app,
     'tags': 'note',
     'description': 'Ask to create a note e.g. "Jarvis can you open a note"?'
     },

    {'name': 'open_new_browser_window',
     'enable': True,
     'func': LinuxAppSkills.open_new_browser_window,
     'tags': 'firefox, open firefox',
     'description': 'Ask to open new browser window e.g. "Jarvis can you open a firefox"?'
     },

    {'name': 'open_new_bash',
     'enable': True,
     'func': LinuxAppSkills.open_new_bash,
     'tags': 'bash',
     'description': 'Ask to open new bash e.g. "Jarvis can you open bash"?'
     },

    {'name': 'get_current_location',
     'enable': True,
     'func': LocationSkill.get_current_location,
     'tags': 'my location, current location',
     'description': 'Ask to tell you your current location e.g. "Jarvis tell me my location"?'
     },

    {'name': 'show_history_log',
     'enable': True,
     'func': HistorySkills.show_history_log,
     'tags': 'history, history log, user history',
     'description': 'Ask to tell you asked commands e.g. "Jarvis tell me my history"?'
     },

    {'name': 'learn',
     'enable': True,
     'func': Learn.learn,
     'tags': 'learn new skills, learn',
     'description': 'Learn e.g. "Jarvis learn"'
     },

    {'name': 'tell_response',
     'enable': True,
     'func': Learn.tell_response,
     'tags': '',
     'description': 'Util skill, there is no tags to call it'
     },

     {'name': 'clear_console',
      'enable': True,
      'func': UtilSkills.clear_console,
      'tags': 'clear, clear console',
      'description': 'clears bash console e.g "Jarvis clean console"'
      }
]

skill_objects = {skill['func'].__name__: skill['func'] for skill in BASIC_SKILLS + CONTROL_SKILLS}


# ----------------------------------------------------------------------------------------------------------------------
# Load skills in MongoDB
# ----------------------------------------------------------------------------------------------------------------------

# -------------------------
# Pre-loading processing
# -------------------------
def _convert_skill_object_to_str(skill):
    for sk in skill:
        sk.update((k, v.__name__) for k, v in sk.items() if k == 'func')


_convert_skill_object_to_str(CONTROL_SKILLS)

# Create enable basic skills
ENABLED_BASIC_SKILLS = [skill for skill in BASIC_SKILLS if skill['enable']]
_convert_skill_object_to_str(ENABLED_BASIC_SKILLS)

# -------------------------
# Loading
# -------------------------
all_skills = {
    'control_skills': CONTROL_SKILLS,
    'enabled_basic_skills': ENABLED_BASIC_SKILLS,
}
for collection, documents in all_skills.items():
    db.update_collection(collection, documents)
