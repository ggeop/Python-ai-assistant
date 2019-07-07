# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import wikipedia
import requests
import logging
import time
import re
import urllib.request
import subprocess

from bs4 import BeautifulSoup as bs

from jarvis.skills.skill_manager import AssistantSkill


class BrowserSkills(AssistantSkill):

    @classmethod
    def tell_me_about(cls, voice_transcript, skill):
        """
        Tells about something by searching in wikipedia
        :param voice_transcript: string (e.g 'about google')
        :param skill: dict (e.g
        """
        tags = cls._extract_tags(voice_transcript, skill['tags'])
        for tag in tags:
            reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    response = cls._decoded_wiki_response(topic)
                    cls.response(response)
            except Exception as e:
                logging.debug(e)
                cls.response(" I can't find on the internet what you want")

    @classmethod
    def open_in_youtube(cls, voice_transcript, skill):
        """
        Open a video in youtube.
        :param voice_transcript: string (e.g 'about google')
        :param skill: dict (e.g
        """
        tags = cls._extract_tags(voice_transcript, skill['tags'])
        for tag in tags:
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
                    subprocess.Popen(["python", "-m", "webbrowser", "-t", video], stdout=subprocess.PIPE, shell=False)
            except Exception as e:
                logging.debug(e)
                cls.response("I can't find what do you want in Youtube..")

    @classmethod
    def open_website_in_browser(cls, voice_transcript, skill):
        """
        Opens a web page in the browser.
        :param voice_transcript: string (e.g 'about google')
        :param skill: dict (e.g

        NOTE: If in the voice_transcript there are more than one commands_dict
        e.g voice_transcript='open youtube and open netflix' the application will find
        and execute only the first one, in our case will open the youtube.
        """
        tags = cls._extract_tags(voice_transcript, skill['tags'])
        for tag in tags:
            reg_ex = re.search(tag + ' ([a-zA-Z]+)', voice_transcript)
            try:
                if reg_ex:
                    domain = reg_ex.group(1)
                    url = cls._create_url(domain)
                    cls.response('Sure')
                    subprocess.Popen(["python", "-m", "webbrowser", "-t", url], stdout=subprocess.PIPE, shell=False)
                    time.sleep(1)
                    cls.response('I opened the {0}'.format(domain))
            except Exception as e:
                logging.debug(e)
                cls.response("I can't find this domain..")

    @classmethod
    def tell_me_today_news(cls, **kwargs):
        try:
            news_url = "https://news.google.com/news/rss"
            client = urllib.request.urlopen(news_url)
            xml_page = client.read()
            client.close()
            soup = bs(xml_page, "xml")
            news_list = soup.findAll("item")
            for news in news_list[:5]:
                response = ""
                data = news.title.text.encode('utf-8')
                response += data.decode()
                cls.response(response)
        except Exception as e:
            logging.debug(e)

    @classmethod
    def _decoded_wiki_response(cls, topic):
        """
        A private method for decoding the wiki response.
        :param topic: string
        :return: string
        """
        ny = wikipedia.page(topic)
        data = ny.content[:500].encode('utf-8')
        response = ''
        response += data.decode()
        return response

    @classmethod
    def _create_url(cls, tag):
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

