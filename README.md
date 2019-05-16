# Jarvis (Voice Assistant)

# Dependencies

# Features
* Continues listening service, triggered by 'hello'
* Search on the internet
* Launch applications
* Tells the time

### SOON Features
* Tells the weather
* Play a song from youtube
* Can spell a word
* Keep a note

# Processing Components
```
voice--> text--> extract commands--> execute commands--> results -->speech
```
* ```voice--> text```
For voice recognition we used google recognition API

* ```text--> extract commands```
This component extract specific commands from the free text.

# How it works
Start and run voice assistant service in the background.
``` nohup assistant.py >/dev/null 2>&1 &```
