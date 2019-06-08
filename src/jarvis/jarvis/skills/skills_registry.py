from jarvis.skills.skill_manager import SkillManager


"""
All available assistant skills
Keys description:
    - 'enable': boolean (With True are the enabled skills)
    - 'skill': The skill method in SkillManager
    - 'tags': The available triggering tags
    - 'description': skill description
"""


CONTROL_SKILLS = {
    'enable_jarvis': {'skill': SkillManager.enable_jarvis,
                      'tags': {'start', 'hi', 'hello', 'jarvis'}
                      },

    'disable_jarvis': {'skill': SkillManager.disable_jarvis,
                       'tags': {'bye', 'stop', 'shut down'}
                       }
}


BASIC_SKILLS = {
    'open_browser': {'enable': True,
                     'skill': SkillManager.open_website_in_browser,
                     'tags': {'open'},
                     'description': 'Ask me to "open" a domain in the browser e.x open facebook'
                     },

    'tell_time': {'enable': True,
                  'skill': SkillManager.tell_the_time,
                  'tags': {'time', 'hour'},
                  'description': 'Ask me for the current "time"'
                  },

    'tell_about': {'enable': True,
                   'skill': SkillManager.tell_me_about,
                   'tags': {'about'},
                   'description': 'Ask me "about" something, e.g. tell me about google'
                   },

    'current_weather': {'enable': True,
                        'skill': SkillManager.tell_the_weather,
                        'tags': {'weather', 'tell me the weather'},
                        'description': 'Ask for the "weather in" somewhere, e.g. weather in London'
                        },
    'assistant_check': {'enable': True,
                        'skill': SkillManager.assistant_check,
                        'tags': {'hi', 'jarvis', 'hear', 'can you hear', 'hey jarvis'},
                        'description': 'Ask me if I "hear" you, e.g. Jarvis "can you hear" me?'
                        },
    'open_libreoffice_calc': {'enable': True,
                              'skill': SkillManager.open_libreoffice_calc,
                              'tags': {'open calc', 'open excel', 'calc', 'excel'},
                              'description': 'Ask me to "open writer", e.g. Jarvis "can you open calc"?'
                              },
    'open_libreoffice_writer': {'enable': True,
                                'skill': SkillManager.open_libreoffice_writer,
                                'tags': {'open writer', 'open word', 'writer', 'word'},
                                'description': 'Ask me to "open writer", e.g. Jarvis "can you open writer"?'
                               },
    'open_libreoffice_impress': {'enable': True,
                                'skill': SkillManager.open_libreoffice_impress,
                                'tags': {'open impress', 'open power point', 'impress', 'power point'},
                                'description': 'Ask me to "open impress", e.g. Jarvis "can you open impress"?'
                                },
    'tell_memory_consumption': {'enable': True,
                                'skill': SkillManager.tell_memory_consumption,
                                'tags': {'ram', 'ram usage', 'memory', 'memory consumption', 'are you busy'},
                                'description': 'Ask for the memory consumption, '
                                               'e.g. Jarvis how much "memory" are you using?'
                                },
    'open_in_youtube': {'enable': True,
                        'skill': SkillManager.open_in_youtube,
                        'tags': {'open in youtube', 'find in youtube', 'play in youtube'},
                        'description': 'Ask for the memory consumption, e.g. Jarvis how much "memory" are you using?'
                        },

}

ADVANCE_SKILLS = {}