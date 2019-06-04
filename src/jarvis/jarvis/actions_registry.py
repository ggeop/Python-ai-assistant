from jarvis.action_manager import ActionManager


"""
All available assistant actions
Keys description:
    - 'enable': boolean (With True are the enabled actions)
    - 'action': The action method in ActionManager
    - 'tags': The available triggering tags
    - 'description': Method description
"""

ACTIONS = {
    'open_browser': {'enable': True,
                     'action': ActionManager.open_website_in_browser,
                     'tags': {'open'},
                     'description': 'Ask me to "open" a domain in the browser e.x open facebook'
                     },

    'tell_time': {'enable': True,
                  'action': ActionManager.tell_the_time,
                  'tags': {'time', 'hour'},
                  'description': 'Ask me for the current "time"'
                  },

    'tell_about': {'enable': True,
                   'action': ActionManager.tell_me_about,
                   'tags': {'about'},
                   'description': 'Ask me "about" something, e.g. tell me about google'
                   },

    'current_weather': {'enable': True,
                        'action': ActionManager.tell_the_weather,
                        'tags': {'weather'},
                        'description': 'Ask for the "weather in" somewhere, e.g. weather in London'
                        },
    'assistant_check': {'enable': True,
                        'action': ActionManager.assistant_check,
                        'tags': {'hear', 'can you hear', 'hey jarvis'},
                        'description': 'Ask me if I "hear" you, e.g. Jarvis "can you hear" me?'
                        },

}


CONTROL_ACTIONS = {
    'enable_jarvis': {'action': ActionManager.enable_jarvis,
                      'tags': {'start', 'hi', 'hello', 'jarvis'}
                      },

    'disable_jarvis': {'action': ActionManager.disable_jarvis,
                       'tags': {'stop', 'shut down'}
                       }
}
