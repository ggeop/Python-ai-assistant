from jarvis.skills import \
    word_skills,\
    assistant_activation,\
    assistant_info_skills, \
    reminder_skill,\
    libreoffice_suite_skills, \
    internet_skills,\
    browser_skills,\
    system_health_skills,\
    datetime_skill,\
    weather_skills

"""
All available assistant skills
Keys description:
    - 'enable': boolean (With True are the enabled skills)
    - 'skill': The skill method in Skills
    - 'tags': The available triggering tags
    - 'description': skill description
"""


CONTROL_SKILLS = {
    'enable_jarvis': {'skill': assistant_activation.enable_jarvis,
                      'tags': {'start', 'hi', 'hello', 'jarvis'}
                      },

    'disable_jarvis': {'skill': assistant_activation.disable_jarvis,
                       'tags': {'bye', 'stop', 'shut down'}
                       }
}


BASIC_SKILLS = {
    'open_browser': {'enable': True,
                     'skill': browser_skills.open_website_in_browser,
                     'tags': {'open'},
                     'description': 'Ask me to "open" a domain in the browser e.x open facebook'
                     },

    'tell_time': {'enable': True,
                  'skill': datetime_skill.tell_the_time,
                  'tags': {'time', 'hour'},
                  'description': 'Ask me for the current "time"'
                  },
    'tell_date': {'enable': True,
                  'skill': datetime_skill.tell_the_date,
                  'tags': {'date'},
                  'description': 'Ask me for the current "date"'
                  },
    'tell_about': {'enable': True,
                   'skill': browser_skills.tell_me_about,
                   'tags': {'about'},
                   'description': 'Ask me "about" something, e.g. tell_the_skills me about google'
                   },

    'current_weather': {'enable': True,
                        'skill': weather_skills.tell_the_weather,
                        'tags': {'weather', 'tell_the_skills me the weather'},
                        'description': 'Ask for the "weather in" somewhere, e.g. weather in London'
                        },
    'assistant_info_skills': {'enable': True,
                        'skill': assistant_info_skills.assistant_check,
                        'tags': {'hi', 'hear', 'can you hear', 'hey jarvis', 'are you there'},
                        'description': 'Ask me if I "hear" you, e.g. Jarvis "can you hear" me?'
                        },
    'libreoffice_suite_skills': {'enable': True,
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
    'system_health_skills': {'enable': True,
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
    'internet_skills': {'enable': True,
                        'skill': internet_skills.run_speedtest,
                        'tags': {'speedtest', 'internet speed', 'ping'},
                        'description': 'Ask for internet speedtest, e.g. Jarvis tell_the_skills me the "internet speed"?'
                        },
    'word_skills': {'enable': True,
                    'skill': word_skills.spell_a_word,
                    'tags': {'spell', 'spell the word'},
                    'description': 'Ask to spell a word, e.g. Jarvis can you spell the word "animal"?'
                     },
    'reminder_skill': {'enable': True,
                        'skill': reminder_skill.create_reminder,
                        'tags': {'remind', 'remind me'},
                        'description': 'Ask to remind you something e.g. "Jarvis create a 5 minute reminder"?'
                       },
    'tell_the_skills': {'enable': True,
                        'skill': assistant_info_skills.tell_the_skills,
                        'tags': {'skills', 'your skills', 'what can you do', 'what are your skills'},
                        'description': 'Ask to remind you something e.g. "Jarvis create a 5 minute reminder"?'
                       },

}

ADVANCE_SKILLS = {}
