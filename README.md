![alt text](https://github.com/ggeop/Jarvis-voice-assistant/blob/development/imgs/jarvis_logo.png)

Jarvis is a voice assistant service in [Python 3.4+](https://www.python.org/downloads/release/python-360/)
It can understand human speech, talk to user and execute basic commands.

## Features
* **Continues listening service**, triggered by a phrase e.g ('hi', 'hello jarvis')
* **Opens a web page** (e.g Jarvis open youtube)
* **Opens libreoffice suite applications** (calc, writer, impress)
* **Tells about something**, by searching on the internet (e.g Jarvis tells me about oranges)
* **Tells the weather** for a place (e.g Jarvis tell me the weather in London)
* **Tells the current time** (e.g Jarvis tells me time)
* **Uses wolfram API** for general questions
* Easy **voice-command customization**
* **Vocal or/and text response**

### How to add a new feature
You can easily add a new feature in two steps.
* Create a new configuration in ACTION in **actions_registry.py**
```{python}
'new_action': {'enable': True,
                 'action': ActionManager.new_action,
                 'tags': {'tag1', 'tag2'},
                 'description': 'action description..'
                },                
```
* Create a new method in **action_manager.py**
```
@classmethod
    def new_action(cls,**kargs):
      pass
```
Now you can test it!

## Desicion Model
![alt text](https://github.com/ggeop/Jarvis/blob/master/imgs/desicion_model.png)

## Getting Started
### Create KEYs for third party APIs
Jarvis assistant uses third party APIs for speech recognition,web information search, weather forecasting etc.
All the following APIs have free no-commercial API calls. Subscribe to the following APIs in order to take access KEYs.
* [OpenWeatherMap](https://openweathermap.org/appid): API for weather forecast.
* [WolframAlpha](https://developer.wolframalpha.com/portal/myapps/): API for answer questions.

### Download the code in your Ubundu/Debian system!
* Go to home directory:

```
cd ~/
```
* Download the Jarvis repo localy:

```
git clone https://github.com/ggeop/Jarvis.git
```

### Create Virtual Env
The first step is to setup the virtual environment with the project dependencies.
* If you don't have installed the virtualenv package, you can install it with pip:
```
pip install virtualenv
```
* Create a virtual environment
* We create a new virtual environment inside the Jarvis directory:
```
virtualenv ~/Jarvis/py_env
```

### Install Python Dependencies
* Activate the virtual environment:
```
source ~/Jarvis/py_env/bin/activate
```
* Install all the Python packages in your:
```
pip install -r requirements.txt
```

### Put the Keys in settings
* Before you start running the application you have to put the free KEYs in the settings.py:
```
nano Jarvis/src/jarvis/jarvis/setting.py
```

### Start voice assistant
* Start the assistant service:
```
python Jarvis/src/jarvis/start.py
```

* (OR) start the assistant service in the background:
```
nohup python Jarvis/src/jarvis/start.py >/dev/null 2>&1 &
```

---

### Jarvis Screenshots
* [A quick look of Jarvis console output](https://github.com/ggeop/Jarvis/blob/master/imgs/Jarvis_printscreen.PNG)

* [Behind the scenes](https://github.com/ggeop/Jarvis/blob/master/imgs/jarvis_log.PNG)
