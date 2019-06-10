import re
import subprocess
import logging
import requests
from bs4 import BeautifulSoup as bs

from jarvis.utils.response_utils import assistant_response


def open_in_youtube(tag, voice_transcript, **kwargs):
    """
    Open a video in youtube.
    :param tag: string (e.g 'open')
    :param voice_transcript: string (e.g 'open in youtube tdex')
    """
    # TODO:  Replace with YOUTUBE API
    reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
    try:
        if reg_ex:
            search_text = reg_ex.group(1)
            base = "https://www.youtube.com/results?search_query=" + "&orderby=viewCount"
            r = requests.get(base + search_text.replace(' ', '+'))
            page = r.text
            soup = bs(page, 'html.parser')
            vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
            video = 'https://www.youtube.com' + vids[0]['href']
            subprocess.Popen(["python", "-m", "webbrowser", "-t", video], stdout=subprocess.PIPE)
    except Exception as e:
        logging.debug(e)
        assistant_response("I can't find what do you want in Youtube..")