import re
import time
import logging

from jarvis.core.response import assistant_response


def spell_a_word(tag, voice_transcript, **kwargs):
    """
    Spell a words letter by letter.
    :param tag: string (e.g 'spell the word')
    :param voice_transcript: string (e.g 'spell the word animal')
    """
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            search_text = reg_ex.group(1)
            for letter in search_text:
                assistant_response(letter)
                time.sleep(2)
    except Exception as e:
        logging.debug(e)
        assistant_response("I can't spell the word")
