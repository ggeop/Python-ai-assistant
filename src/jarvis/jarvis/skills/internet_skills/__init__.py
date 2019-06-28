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

import subprocess
import json
import requests
import logging

from jarvis.core.response import assistant_response


def _decode_json(response_bytes):
    json_response = response_bytes.decode('utf8').replace("'", '"')
    return json.loads(json_response)


def run_speedtest(**kwargs):
    """
    Run an internet speed test.
    """
    process = subprocess.Popen(["speedtest-cli", "--json"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:

        decoded_json = _decode_json(out)

        ping = decoded_json['ping']
        up_mbps = float(decoded_json['upload']) / 1000000
        down_mbps = float(decoded_json['download']) / 1000000

        assistant_response("Speedtest results:\n"
                           "The ping is %s ms \n"
                           "The upling is %0.2f Mbps \n"
                           "The downling is %0.2f Mbps" % (ping, up_mbps, down_mbps)
                           )
    else:
        assistant_response("I coudn't run a speedtest")
        logging.error("Speedtest error with message: {0}".format(err))


def internet_availability(**kwargs):
    """
    Tells to the user is the internet is available or not
    """
    try:
        _ = requests.get('http://www.google.com/', timeout=1)
        assistant_response("Yes, the internet connection is ok")
    except requests.ConnectionError as e:
        assistant_response("No the internet is down for now")
        logging.error("No internet connection with message: {0}".format(e))
