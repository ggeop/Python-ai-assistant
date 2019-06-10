import subprocess
import json
import requests
import logging

from jarvis.utils.response_utils import assistant_response


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


def internet_availability(**kwargs):
    """
    Tells to the user is the internet is available or not
    """
    try:
        _ = requests.get('http://www.google.com/', timeout=1)
        assistant_response("Yes, the internet connection is ok")
    except requests.ConnectionError:
        assistant_response("No the internet is down for now")
