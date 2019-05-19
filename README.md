![alt text](https://github.com/ggeop/Jarvis/blob/master/jarvis_logo.png)

Jarvis is a voice assistant service. It can understand human speech, talk to user and execute basic commands

# Dependencies
* Linux Ubundu
* Python 3.5 +

# Features
* Continues listening service, triggered by a phrase e.g ('hi', 'hello jarvis')
* Opens a web page
* Tells about something, by searching on the internet
* Tells the weather
* Tells the time

# How it works
* Run voice assistant service.
``` python run.py &```

* Run Jarvis service in the background.
``` nohup python run.py >/dev/null 2>&1 &```
