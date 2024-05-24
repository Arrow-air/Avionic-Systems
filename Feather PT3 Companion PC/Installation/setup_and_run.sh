#!/bin/bash

# Step 1: Enable UART and SPI then reboot
echo "Enabling SPI and rebooting..."
sudo bash enable_uart_spi.sh

echo "After reboot, please run the following commands manually:"
echo "1. sudo bash install_dependencies.sh"
echo "2. sudo bash configure_can.sh"
echo "3. bash run_project.sh"
