![alt text](https://github.com/ggeop/Jarvis/blob/master/jarvis_logo.png)

## About Jarvis
Jarvis is a voice assistant service in [Python 3.4+](https://www.python.org/downloads/release/python-360/)
It can understand human speech, talk to user and execute basic commands.

---

## Install Python Dependencies
```
pip install -r requirements.txt
```
---

## Features
* Continues listening service, triggered by a phrase e.g ('hi', 'hello jarvis')
* Opens a web page (e.g Jarvis open youtube)
* Tells about something, by searching on the internet (e.g Jarvis tells me about oranges)
* Tells the weather for a place (e.g Jarvis tell me the weather in London)
* Tells the current time (e.g Jarvis tells me time)
* Easy voice-command costumization
* Vocal or/and text response 

---

## How it works
* Run voice assistant service:
``` python run.py```

* Run Jarvis service in the background:
``` nohup python run.py >/dev/null 2>&1 &```
