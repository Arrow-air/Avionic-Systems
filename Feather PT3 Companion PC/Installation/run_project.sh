#!/bin/bash

# Pls Navigate to your project directory
cd /home/alexdada/Documents/Avionic-Systems/Feather\ PT3\ Companion\ PC/

# Run Backend Data handler
sudo python3 FCPC.py

# Run System State Window Frontend
sudo python3 main_2screens_2displays.py &

# Run System Information Window Frontend
sudo python3 main_2screens_2displays2.py &
