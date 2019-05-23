from jarvis.action_manager import ActionManager
from collections import OrderedDict


# All available assistant actions
ACTIONS = OrderedDict({
    'enable_jarvis': {'action': ActionManager.enable_jarvis,
                      'tags': ['start', 'hi', 'jarvis']},

    'open_browser': {'action': ActionManager.open_website_in_browser,
                     'tags': ['open', 'do']},

    'tell_time': {'action': ActionManager.tell_the_time,
                  'tags': ['time']},

    'tell_about': {'action': ActionManager.tell_me_about,
                   'tags': ['about']},

    'current_weather': {'action': ActionManager.tell_the_weather,
                        'tags': ['weather']},

    'disable_jarvis': {'action': ActionManager.disable_jarvis,
                       'tags': ['stop', 'shut down']},
})
