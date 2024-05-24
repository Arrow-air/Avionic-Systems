#!/bin/bash

# Enable UART
if ! grep -q "^enable_uart=1" /boot/firmware/config.txt; then
    echo "enable_uart=1" | sudo tee -a /boot/firmware/config.txt
fi

# Enable SPI
if ! grep -q "^dtparam=spi=on" /boot/firmware/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/firmware/config.txt
fi

# Append additional configuration for CAN
sudo tee -a /boot/firmware/config.txt <<EOF
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=25
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=23
dtoverlay=spi-bcm2835-overlay
EOF

# Reboot
sudo reboot
