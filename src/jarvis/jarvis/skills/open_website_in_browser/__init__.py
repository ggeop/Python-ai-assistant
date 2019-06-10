import logging
import time
import re
import subprocess
from jarvis.utils.response_utils import assistant_response


def _create_url(tag):
    """
    Creates a url. It checks if there is .com suffix and add it if it not exist.
    :param tag: string (e.g youtube)
    :return: string (e.g http://www.youtube.com)
    """
    if re.search('.com', tag):
        url = 'http://www.' + tag
    else:
        url = 'http://www.' + tag + '.com'
    return url


def open_website_in_browser(tag, voice_transcript, **kwargs):
    """
    Opens a web page in the browser.
    :param tag: string (e.g 'open')
    :param voice_transcript: string (e.g 'open youtube')

    NOTE: If in the voice_transcript there are more than one commands_dict
    e.g voice_transcript='open youtube and open netflix' the application will find
    and execute only the first one, in our case will open the youtube.
    """
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            domain = reg_ex.group(1)
            url = _create_url(domain)
            assistant_response('Sure')
            subprocess.Popen(["python", "-m", "webbrowser", "-t", url], stdout=subprocess.PIPE)
            time.sleep(1)
            assistant_response('I opened the {0}'.format(domain))
    except Exception as e:
        logging.debug(e)
        assistant_response("I can't find this domain..")


