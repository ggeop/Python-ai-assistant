from jarvis.action_manager import ActionManager


# All available assistant actions
ACTIONS = {
    'open_browser': {'enable': True,
                     'action': ActionManager.open_website_in_browser,
                     'tags': set('open', 'do')},

    'tell_time': {'enable': True,
                  'action': ActionManager.tell_the_time,
                  'tags': set('time')},

    'tell_about': {'enable': True,
                   'action': ActionManager.tell_me_about,
                   'tags': set('about')},

    'current_weather': {'enable': True,
                        'action': ActionManager.tell_the_weather,
                        'tags': set('weather')},
}

CONTROL_ACTIONS = {
    'enable_jarvis': {'action': ActionManager.enable_jarvis,
                      'tags': set('start', 'hi', 'jarvis')},

    'disable_jarvis': {'action': ActionManager.disable_jarvis,
                       'tags': set('stop', 'shut down')},
}
