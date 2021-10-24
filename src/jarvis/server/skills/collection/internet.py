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

import requests
import logging
import speedtest

from jarvis.skills.skill import AssistantSkill
from jarvis.utils.startup import internet_connectivity_check


class InternetSkills(AssistantSkill):

    @classmethod
    def run_speedtest(cls, **kwargs):
        """
        Run an internet speed test. Speed test will show
        1) Download Speed
        2) Upload Speed
        3) Ping
        """
        try:
            cls.response("Sure! wait a second to measure")
            st = speedtest.Speedtest()
            server_names = []
            st.get_servers(server_names)

            downlink_bps = st.download()
            uplink_bps = st.upload()
            ping = st.results.ping
            up_mbps = uplink_bps / 1000000
            down_mbps = downlink_bps / 1000000

            cls.response("Speedtest results:\n"
                         "The ping is: %s ms \n"
                         "The upling is: %0.2f Mbps \n"
                         "The downling is: %0.2f Mbps" % (ping, up_mbps, down_mbps)
                         )

        except Exception as e:
            cls.response("I coudn't run a speedtest")
            logging.error("Speedtest error with message: {0}".format(e))

    @classmethod
    def internet_availability(cls, **kwargs):
        """
        Tells to the user is the internet is available or not.
        """
        if internet_connectivity_check():
            cls.response("The internet connection is ok")
            return True
        else:
            cls.response("The internet is down for now")
            return False
