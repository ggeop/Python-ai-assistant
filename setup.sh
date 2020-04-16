#!/usr/bin/env bash

# -----------------------------------
# Initialization
# -----------------------------------
JARVIS_DIR=$(pwd)
VIRTUAL_ENV="jarvis_virtualenv"

green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

# -----------------------------------
# Python version compatibility check
# -----------------------------------
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "${red} No Python 3.x.x in your system! Install Python and try again! ${reset}"
    exit 1
else
    PYTHON_PATH=$(which python3)
fi



#-----------------------------------
# System dependencies installation
#-----------------------------------
sudo apt-get update && /
sudo apt-get install python-dev && /
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio && /
sudo apt-get install libasound2-plugins libsox-fmt-all libsox-dev sox ffmpeg && /
sudo apt-get install espeak && /
sudo apt-get install python3-pip && /
sudo apt-get install python3-setuptools

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} System dependencies installation succeeded! ${reset}"
else
    echo "${red} System dependencies installation failed ${reset}"
    exit 1
fi


#-----------------------------------
# Install virtualenv
#-----------------------------------
pip3 install virtualenv

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install virtualenv succeeded! ${reset}"
else
    echo "${red} Install virtualenv failed ${reset}"
    exit 1
fi

#-----------------------------------
# Create Jarvis virtual env
#-----------------------------------
virtualenv -p $PYTHON_PATH $JARVIS_DIR/$VIRTUAL_ENV

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Jarvis virtual env creation succeeded! ${reset}"
else
    echo "${red} Jarvis virtual env creation failed ${reset}"
    exit 1
fi

#-----------------------------------
# Install Python dependencies
#-----------------------------------
source $JARVIS_DIR/$VIRTUAL_ENV/bin/activate

# Install pip in virtualenv
sudo apt-get install python3-pip

# Install python requirements
pip3 install -r $JARVIS_DIR/requirements.txt

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install Python dependencies succeeded! ${reset}"
else
    echo "${red} Install Python dependencies failed ${reset}"
    exit 1
fi

#-----------------------------------
# Install nltk dependencies
#-----------------------------------
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install nltk dependencies succeeded! ${reset}"
else
    echo "${red} Install nltk dependencies failed ${reset}"
    exit 1
fi

#-----------------------------------
# Create log access
#-----------------------------------
sudo touch /var/log/jarvis.log && \
sudo chmod 777 /var/log/jarvis.log

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Create log access succeeded! ${reset}"
else
    echo "${red}Create log access failed ${reset}"
    exit 1
fi

#-----------------------------------
# Deactivate virtualenv
#-----------------------------------
deactivate

#-----------------------------------
# Install MongoDB Server
#-----------------------------------
# Install process: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

# Install gnupg
sudo apt-get install gnupg

# MongoDB public GPG Key
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# Create the /etc/apt/sources.list.d/mongodb-org-4.2.list file for Ubuntu 16.04 (Xenial):
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

# Reload local package database
sudo apt-get update

# Install a specific release of MongoDB
sudo apt-get install -y mongodb-org=4.2.5 mongodb-org-server=4.2.5 mongodb-org-shell=4.2.5 mongodb-org-mongos=4.2.5 mongodb-org-tools=4.2.5

# Create alias in .bashrc
echo >> ~/.bashrc
echo >> "# Create alias for Jarvis assistant"
echo "alias jarvis='bash ${JARVIS_DIR}/run_jarvis.sh'"
echo >> ~.bashrc
source ~/.bashrc

#-----------------------------------
# Finished
#-----------------------------------
echo "${green} Jarvis setup succeed! ${reset}"
echo "Start Jarvis: bash run_jarvis.sh"