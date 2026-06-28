#!/usr/bin/with-contenv bash

echo "########################################"
echo "ESP32 CAMERA BRIDGE STARTED"
echo "########################################"

ls -l /

echo "Python:"
which python3
python3 --version

echo "Pip packages:"
python3 -m pip list

sleep 300
