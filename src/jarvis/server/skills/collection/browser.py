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
import time
import re
import urllib.request
import subprocess
import webbrowser

from bs4 import BeautifulSoup as bs

from jarvis.skills.skill import AssistantSkill


class BrowserSkills(AssistantSkill):

    @classmethod
    def tell_me_about(cls, voice_transcript, skill):
        """
        Tells about something by searching on wiki.
        :param voice_transcript: string (e.g 'about google')
        :param skill: dict
        """
        tags = cls.extract_tags(voice_transcript, skill['tags'])
        only_text_pattern = '([a-zA-Z]+)'
        for tag in tags:
            reg_ex = re.search(tag + ' ' + only_text_pattern, voice_transcript)
            if reg_ex:
                topic = reg_ex.group(1)
                try:
                    response = cls._decoded_wiki_response(topic)
                    cls.response(response)
                except Exception as e:
                    cls.console(error_log="Error with the execution of skill with message {0}".format(e))
                    cls.response(" I can't find what you want, and I will open a new tab in browser")
                    time.sleep(1)
                    cls._search_on_google(topic)

    @classmethod
    def open_in_youtube(cls, voice_transcript, skill):
        """
        Open a video in youtube.
        :param voice_transcript: string (e.g 'play mozart')
        :param skill: dict (e.g
        """

        tags = cls.extract_tags(voice_transcript, skill['tags'])
        for tag in tags:
            reg_ex = re.search(tag + ' (.*)', voice_transcript)

            try:
                if reg_ex:
                    search_text = reg_ex.group(1)
                    base = "https://www.youtube.com/results?search_query={0}&orderby=viewCount"
                    r = requests.get(base.format(search_text.replace(' ', '+')))
                    page = r.text
                    soup = bs(page, 'html.parser')
                    vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
                    video = 'https://www.youtube.com' + vids[0]['href'] + "&autoplay=1"
                    cls.console(info_log="Play Youtube video: {0}".format(video))
                    subprocess.Popen(["python", "-m", "webbrowser", "-t", video], stdout=subprocess.PIPE, shell=False)
            except Exception as e:
                cls.console(error_log="Error with the execution of skill with message {0}".format(e))
                cls.response("I can't find what do you want in Youtube..")

    @classmethod
    def open_website_in_browser(cls, voice_transcript, skill):
        """
        Opens a web page in the browser.
        :param voice_transcript: string (e.g 'about google')
        :param skill: dict (e.g

        Web page can be in the following formats
          * open www.xxxx.com
          *  open xxxx.com
          *  open xxxx

        Limitations
        - If in the voice_transcript there are more than one commands_dict
          e.g voice_transcript='open youtube and open netflix' the application will find
          and execute only the first one, in our case will open the youtube.
        - Support ONLY the following top domains: '.com', '.org', '.net', '.int', '.edu', '.gov', '.mil'

        """
        tags = cls.extract_tags(voice_transcript, skill['tags'])
        domain_regex = '([\.a-zA-Z]+)'
        ""
        for tag in tags:
            reg_ex = re.search(tag + ' ' + domain_regex, voice_transcript)
            try:
                if reg_ex:
                    domain = reg_ex.group(1)
                    url = cls._create_url(domain)
                    cls.response('Sure')
                    time.sleep(1)
                    webbrowser.open_new_tab(url)
                    cls.response('I opened the {0}'.format(domain))
            except Exception as e:
                cls.console(error_log="Error with the execution of skill with message {0}".format(e))
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
            response = ""
            for news in news_list[:5]:
                data = news.title.text.encode('utf-8') + '\n'
                response += data.decode()
            cls.response(response)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("I can't find about daily news..")

    @classmethod
    def _decoded_wiki_response(cls, topic):
        """
        Decoding the wiki response.
        :param topic: string
        :return: string
        """
        ny = wikipedia.page(topic)
        data = ny.content[:500].encode('utf-8')
        response = ''
        response += data.decode()
        return response

    @classmethod
    def _create_url(cls, domain):
        """
        Creates a url. It checks if there is .com suffix and add it if it not exist.
        :param tag: string (e.g youtube)
        :return: string (e.g http://www.youtube.com)
        """
        top_level_domains = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil']
        url = None
        for top_level_domain in top_level_domains:
            if re.search(top_level_domain, domain):
                url = 'http://' + domain

        url = 'http://www.' + domain + '.com' if not url else url
        return url

    @classmethod
    def _search_on_google(cls, term):
        url = "https://www.google.com.tr/search?q={}".format(term)
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            cls.console(error_log="Error with the execution of skill with message {0}".format(e))
            cls.response("Sorry I faced an issue with google search")

