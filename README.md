[![CodeFactor](https://www.codefactor.io/repository/github/ggeop/python-voice-assistant/badge)](https://www.codefactor.io/repository/github/ggeop/Python-voice-assistant)
[![Maintainability](https://api.codeclimate.com/v1/badges/8c90305e22186cc2c9d5/maintainability)](https://codeclimate.com/github/ggeop/Python-voice-assistant/maintainability)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/ggeop/Python-voice-assistant.svg?branch=master)](https://travis-ci.org/ggeop/Python-voice-assistant)

![alt text](https://github.com/ggeop/Jarvis/blob/master/imgs/Jarvis_printscreen.PNG)

# About
Jarvis is a voice assistant service in [Python 3.5+](https://www.python.org/downloads/release/python-360/)
It can understand human speech, talk to user and execute basic commands.

#### Assistant Skills
*   **Opens a web page** (e.g 'Jarvis open youtube')
*   **Play a video in Youtube** (e.g 'find in you tdex in youtube')
*   **Opens libreoffice suite applications (calc, writer, impress)** (e.g 'Jarvis open calc')
*   **Tells about something**, by searching on the internet (e.g 'Jarvis tells me about oranges')
*   **Tells the weather** for a place (e.g 'Jarvis tell_the_skills me the weather in London')
*   **Tells the current time and/or date** (e.g 'Jarvis tells me time or date')
*   **Tells the internet speed (ping, uplink and downling)** (e.g 'Jarvis tell_the_skills me the internet speed')
*   **Tells the internet availability** (e.g 'Jarvis is the internet connection ok?')
*   **Tells the daily news** (e.g 'Jarvis tell me today news')
*   **Spells a word** (e.g 'Jarvis spell me the word animal')
*   **Creates a reminder** (e.g 'Jarvis create a 10 minutes reminder')
*   **Opens linux applications** (e.g 'Jarvis open bash/firefox')
*   **Tells everything it can do** (e.g 'Jarvis tell me your skills or tell me what can you do')
*   **Tells the current location** (e.g 'Jarvis tell me your current location')
*   **Tells how much memory consumes** (e.g 'Jarvis tell me your memory consumption)

#### Assistant Features
*   **Asynchronous command execution & speech interruption**
*   **Custom wake words**, can be triggered with any word or phrase e.g ('hi', 'hi Jarvis', 'wake up') 
*   **Continues listening service**, triggered by a phrase e.g ('hi', 'hello jarvis')
*   Easy **voice-command customization**
*   Configurable **assistant name** (e.g 'Jarvis', 'Sofia', 'John' etc.)
*   **Log preview** in console
*   **Vocal or/and text response**

## Getting Started
### Create KEYs for third party APIs
Jarvis assistant uses third party APIs for speech recognition,web information search, weather forecasting etc.
All the following APIs have free no-commercial API calls. Subscribe to the following APIs in order to take FREE access KEYs.
*   [OpenWeatherMap](https://openweathermap.org/appid): API for weather forecast.
*   [WolframAlpha](https://developer.wolframalpha.com/portal/myapps/): API for answer questions.
*   [IPSTACK](https://ipstack.com/signup/free): API for current location.
### Setup Jarvis in Ubundu/Debian system
*   Download the Jarvis repo localy:

```bash
git clone https://github.com/ggeop/Jarvis.git
```
*   Setup Jarvis and system dependencies:
```bash
bash setup.sh
```

*   Put the Keys in settings

**NOTE:** *For better exprerience, before you start the application you can put the free KEYs in the settings.py*

```bash
nano Jarvis/src/jarvis/jarvis/setting.py
```

### Start voice assistant
*   Start the assistant service:
```bash
bash run_jarvis.sh
```


### How to add a new Skill
You can easily add a new skill in two steps.
*   Create a new configurationin SKILLS in **skills_registry.py**
```python
'new_skill': {'enable': True,
              'skill': Skills.new_skill,
              'tags': {'tag1', 'tag2'},
              'description': 'skill description..'
              }               
```
*   Create a new skill package in **skills**

### Desicion Model
![alt text](https://github.com/ggeop/Jarvis/blob/master/imgs/desicion_model.png)

### Extract skill
The skill extraction implement in a matrix of [TF-IDF features](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) for each skill.
In the following example he have a dimensional space with three skills.
The user input analyzed in this space and by using a similarity metric (e.g cosine) we find the most similar skill.
![alt text](https://github.com/ggeop/Jarvis/blob/master/imgs/skill_space_desicion.png)



