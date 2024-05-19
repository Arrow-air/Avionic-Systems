#!/bin/bash

# Set up CAN interfaces
sudo ip link set can0 up type can bitrate 500000
sudo ip link set can1 up type can bitrate 250000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can1 txqueuelen 65536

# Check SPI initialization
dmesg | grep spi
