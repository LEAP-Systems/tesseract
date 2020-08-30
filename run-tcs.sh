#!/bin/bash

set -e

OKGREEN='\033[92m'
WARNING='\033[93m'
FAIL='\033[91m'
OKBLUE='\033[94m'
UNDERLINE='\033[4m'
ENDC='\033[0m'

echo "LEAP™ Transmission Control Software"
echo -e "-----------------------------------\n"
echo -e "${UNDERLINE}Development Team:${ENDC}" 
echo -e "Christian Sargusingh | ${OKBLUE}Lead Designer and Systems Engineer${ENDC}"
echo -e "Aaron Huang          | ${OKBLUE}Hardware Engineer${ENDC}"
echo -e "Brandon Zhu          | ${OKBLUE}Software Engineer${ENDC}"
echo -e "Steven Zhou          | ${OKBLUE}QA and Software Engineer${ENDC}"
echo -e "Version: ${OKBLUE}0efde6d3eaaedaa3a20b7c62145d4b3987a98609 @ https://github.com/LEAP-Org/LEAP.git${ENDC}"
echo -e "Updated: ${OKBLUE}2020-07${ENDC}\n"
# setup environment
echo "Setting up environment ..."
export DIM=4
export T_FREQ=30
export HOSTNAME=localhost
export PORT=65432
export SERIAL_PORT=/dev/ttyUSB0
export TCS_ENV=dev

echo -e "Set transmitter dimension to ${OKGREEN}$DIM${ENDC}"
echo -e "Set transmitter frequency to ${OKGREEN}$T_FREQ${ENDC}"
echo -e "Set transmitter address to ${OKGREEN}$HOSTNAME:$PORT${ENDC}"
echo -e "Set transmitter serial out to ${OKGREEN}$SERIAL_PORT${ENDC}"
echo -e "Set tcs environment to ${OKGREEN}$TCS_ENV${ENDC}"
echo -e "${OKGREEN} ✓ ${ENDC}complete "
echo -e "-----------------------------------\n"

# tcs entry
python3 -m tcs