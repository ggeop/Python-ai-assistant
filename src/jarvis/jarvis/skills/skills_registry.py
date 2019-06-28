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

from jarvis.skills import \
    word_skills, \
    assistant_activation, \
    assistant_info_skills, \
    reminder_skill, \
    libreoffice_suite_skills, \
    internet_skills, \
    browser_skills, \
    system_health_skills, \
    datetime_skills, \
    weather_skills, \
    linux_app_skills, \
    location_skill


# All available assistant skills
# Keys description:
#    - 'enable': boolean (With True are the enabled skills)
#    - 'skill': The skill method in Skills
#    - 'tags': The available triggering tags
#    - 'description': skill description

CONTROL_SKILLS = {
    'enable_jarvis': {'skill': assistant_activation.enable_jarvis,
                      'tags': {'start', 'hi', 'hello', 'jarvis'}
                      },

    'disable_jarvis': {'skill': assistant_activation.disable_jarvis,
                       'tags': {'bye', 'shut down'}
                       }
}

BASIC_SKILLS = {
    'open_site_in_browser': {'enable': True,
                             'skill': browser_skills.open_website_in_browser,
                             'tags': {'open'},
                             'description': 'Ask me to "open" a domain in the browser e.x open facebook'
                             },

    'tell_daily_news': {'enable': True,
                        'skill': browser_skills.tell_me_today_news,
                        'tags': {'news', 'today news'},
                        'description': 'Ask me to tell the daily news e.x "Tell me the news today"'
                        },

    'tell_time': {'enable': True,
                  'skill': datetime_skills.tell_the_time,
                  'tags': {'time', 'hour'},
                  'description': 'Ask me for the current "time"'
                  },

    'tell_date': {'enable': True,
                  'skill': datetime_skills.tell_the_date,
                  'tags': {'date'},
                  'description': 'Ask me for the current "date"'
                  },

    'tell_about': {'enable': True,
                   'skill': browser_skills.tell_me_about,
                   'tags': {'about'},
                   'description': 'Ask me "about" something, e.g. tell_the_skills me about google'
                   },

    'assistant_help': {'enable': True,
                       'skill': assistant_info_skills.assistant_help,
                       'tags': {'help'},
                       'description': 'Ask me for "help", e.g. Jarvis help me'
                       },

    'tells_the_weather': {'enable': True,
                          'skill': weather_skills.tell_the_weather,
                          'tags': {'weather', 'tell me the weather'},
                          'description': 'Ask for the "weather in" somewhere, e.g. weather in London'
                          },

    'assistant_check': {'enable': True,
                        'skill': assistant_info_skills.assistant_check,
                        'tags': {'can you hear', 'hey jarvis', 'are you there'},
                        'description': 'Ask me if I "hear" you, e.g. Jarvis "can you hear" me?'
                        },

    'libreoffice_calc': {'enable': True,
                         'skill': libreoffice_suite_skills.open_libreoffice_calc,
                         'tags': {'open calc', 'open excel', 'calc', 'excel'},
                         'description': 'Ask me to "open writer", e.g. Jarvis "can you open calc"?'
                         },

    'open_libreoffice_writer': {'enable': True,
                                'skill': libreoffice_suite_skills.open_libreoffice_writer,
                                'tags': {'open writer', 'open word', 'writer', 'word'},
                                'description': 'Ask me to "open writer", e.g. Jarvis "can you open writer"?'
                                },

    'open_libreoffice_impress': {'enable': True,
                                 'skill': libreoffice_suite_skills.open_libreoffice_impress,
                                 'tags': {'open impress', 'open power point', 'impress', 'power point'},
                                 'description': 'Ask me to "open impress", e.g. Jarvis "can you open impress"?'
                                 },

    'tell_memory_consumption': {'enable': True,
                                'skill': system_health_skills.tell_memory_consumption,
                                'tags': {'ram', 'ram usage', 'memory', 'memory consumption', 'are you busy'},
                                'description': 'Ask for the memory consumption, '
                                               'e.g. Jarvis how much "memory" are you using?'
                                },

    'open_in_youtube': {'enable': True,
                        'skill': browser_skills.open_in_youtube,
                        'tags': {'open in youtube', 'find in youtube', 'play in youtube'},
                        'description': 'Ask for the memory consumption, e.g. Jarvis how much "memory" are you using?'
                        },

    'run_speedtest': {'enable': True,
                      'skill': internet_skills.run_speedtest,
                      'tags': {'speedtest', 'internet speed', 'ping'},
                      'description': 'Ask for internet speedtest, e.g. Jarvis tell_the_skills me the "internet speed"?'
                      },

    'internet_availability': {'enable': True,
                              'skill': internet_skills.internet_availability,
                              'tags': {'internet conection', 'internet is ok', 'do we have internet'},
                              'description': 'Ask for "internet connection", e.g. "Jarvis do we have internet"?'
                              },

    'spell_a_word': {'enable': True,
                     'skill': word_skills.spell_a_word,
                     'tags': {'spell', 'spell the word'},
                     'description': 'Ask to spell a word, e.g. Jarvis can you spell the word "animal"?'
                     },

    'create_reminder': {'enable': True,
                        'skill': reminder_skill.create_reminder,
                        'tags': {'reminder', 'remind me'},
                        'description': 'Ask to remind you something e.g. "Jarvis create a 5 minute reminder"?'
                        },

    'tell_the_skills': {'enable': True,
                        'skill': assistant_info_skills.tell_the_skills,
                        'tags': {'skills', 'your skills', 'what can you do', 'what are your skills'},
                        'description': 'Ask to tell you what he can do e.g. "Jarvis what can you do"?'
                        },
    'take_a_note': {'enable': True,
                    'skill': linux_app_skills.open_note_app,
                    'tags': {'note', 'create a note'},
                    'description': 'Ask to create a note e.g. "Jarvis can you open a note"?'
                    },
    'open_new_browser_window': {'enable': True,
                                'skill': linux_app_skills.open_new_browser_window,
                                'tags': {'firefox', 'open firefox'},
                                'description': 'Ask to open new browser window e.g. "Jarvis can you open a firefox"?'
                                },
    'open_new_bash': {'enable': True,
                      'skill': linux_app_skills.open_new_bash,
                      'tags': {'bash'},
                      'description': 'Ask to open new bash e.g. "Jarvis can you open bash"?'
                      },
    'get_current_location': {'enable': True,
                             'skill': location_skill.get_current_location,
                             'tags': {'my location', 'current location', 'where am I'},
                             'description': 'Ask to tell you your current location e.g. "Jarvis tell me my location"?'
                             },

}

ADVANCE_SKILLS = {}
