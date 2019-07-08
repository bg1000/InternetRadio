#!/bin/bash
cp analog_scanner@pi.service /etc/systemd/system/analog_scanner@${SUDO_USER:-${USER}}.service
sed -i "s?/home/pi/scripts?`pwd`?" /etc/systemd/system/analog_scanner@${SUDO_USER:-${USER}}.service
systemctl --system daemon-reload
systemctl enable analog_scanner@${SUDO_USER:-${USER}}.service
