#!/bin/bash

set -e

$password=leap-ap0
sudo nmcli dev wifi hotspot ifname wlan0 ssid $HOSTNAME password $password