import re
import logging
import wikipedia

from jarvis.utils.response_utils import assistant_response


def _decoded_wiki_response(topic):
    """
    A private method for decoding the wiki response.
    :param topic: string
    :return:
    """
    ny = wikipedia.page(topic)
    data = ny.content[:500].encode('utf-8')
    response = ''
    response += data.decode()
    return response


def tell_me_about(tag, voice_transcript, **kargs):
    """
    Tells about something by searching in wikipedia
    :param tag: string (e.g 'about')
    :param voice_transcript: string (e.g 'about google')
    """
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            response = _decoded_wiki_response(topic)
            assistant_response(response)
    except Exception as e:
        logging.debug(e)
        assistant_response(" I can't find on the internet what you want")