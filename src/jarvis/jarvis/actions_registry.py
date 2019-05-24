from jarvis.action_manager import ActionManager


"""
All available assistant actions
Keys description:
    - 'enable': boolean (With True are the enabled actions)
    - 'action': The action method in ActionManager
    - 'tags': The available triggering tags
"""
ACTIONS = {
    'open_browser': {'enable': True,
                     'action': ActionManager.open_website_in_browser,
                     'tags': {'open'}},

    'tell_time': {'enable': True,
                  'action': ActionManager.tell_the_time,
                  'tags': {'time', 'hour'}},

    'tell_about': {'enable': True,
                   'action': ActionManager.tell_me_about,
                   'tags': {'about'}},

    'current_weather': {'enable': True,
                        'action': ActionManager.tell_the_weather,
                        'tags': {'weather'}},
}


CONTROL_ACTIONS = {
    'enable_jarvis': {'action': ActionManager.enable_jarvis,
                      'tags': {'start', 'hi', 'hello', 'jarvis'}},

    'disable_jarvis': {'action': ActionManager.disable_jarvis,
                       'tags': {'stop', 'shut down'}}
}
