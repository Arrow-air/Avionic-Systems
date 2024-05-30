#!/bin/bash

# Update package list
sudo apt-get update

# Install bcm2835
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz
rm bcm2835-1.60.tar.gz
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
cd ..

# Install wiringPi (for 32-bit and 64-bit systems)
# Uncomment the correct section for your system

# For 32-bit Raspberry Pi system
# sudo apt-get install wiringpi
# wget https://project-downloads.drogon.net/wiringpi-latest.deb
# sudo dpkg -i wiringpi-latest.deb
# gpio -v

# For Bullseye branch
# git clone https://github.com/WiringPi/WiringPi
# cd WiringPi
# sudo ./build
# sudo gpio -v
# cd ..

# For 64-bit Raspberry Pi System
wget https://files.waveshare.com/upload/8/8c/WiringPi-master.zip
sudo apt-get install unzip
unzip WiringPi-master.zip
rm WiringPi-master.zip
cd WiringPi-master/
sudo ./build
cd ..

# Install Python libraries
# Python 2
sudo apt-get install -y python-pip python-pil python-numpy
sudo apt install RPi.GPIO python-spidev python-can

# Python 3
sudo apt-get install -y python3-pip python3-pil python3-numpy
sudo apt install RPi.GPIO python3-spidev python3-can

# Install Pygame and PyQT
sudo apt-get install -y python3-pygame python3-pyqt5
pip install pygame==2.5.2

# Install CAN & Serial library
sudo apt-get install python3-can
sudo apt-get install python3-serial

# Install J1939 CAN Library
pip install can-j1939

# Install Cyphal CAN Library
pip install 'pycyphal[transport-can-pythoncan,transport-serial,transport-udp]'

# Install Library for analysis of DBC files
pip install cantools
