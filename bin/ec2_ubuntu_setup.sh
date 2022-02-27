#!/bin/bash

#
#Author : Chris Boesch
#Date : 08-26-2009
#Purpose : Setup an Amazon EC2 instance and download additional scripts from Github to execute.
#Suggested AMI to develop with: ami-0d729464
#Comments :

set -e -x
export DEBIAN_FRONTEND=noninteractive

function die()
{
    echo -e "$@" >> /dev/console
    exit 1
}

# change the


# adding -y to auto install
# adding unzip command..
apt-get update && apt-get upgrade -y
apt-get -y install unzip


# change TimeZone to Asia/Kolkata
sudo timedatectl set-timezone Asia/Kolkata



# install google chrome
sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
sudo apt -y update
sudo apt -y install google-chrome-stable


# install chromedriver
google-chrome --version

#check the google chrome version and then change the version accordingly
wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

#move the chromedriver file

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

#install chronitor cli

curl -sOL https://cronitor.io/dl/linux_amd64.tar.gz
sudo tar xvf linux_amd64.tar.gz -C /usr/bin/
sudo cronitor configure --api-key b637f3a8b03149eb9d4d4b0d42a5d8dc


#install git
git config --global user.name "your_github_username"
git config --global user.email "your_github_email"
git config -l

git clone https://github.com/dbanerjee1410/stocker.git
#username = <dbanerjee1410>
#passString = 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

git config --global credential.helper cache
git pull -v








