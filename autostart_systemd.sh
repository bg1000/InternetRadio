#!/bin/bash
cp radio_manager@pi.service /etc/systemd/system/radio_manager@${SUDO_USER:-${USER}}.service
sed -i "s?/home/pi/internet_radio?`pwd`?" /etc/systemd/system/radio_manager@${SUDO_USER:-${USER}}.service
systemctl --system daemon-reload
systemctl enable radio_manager@${SUDO_USER:-${USER}}.service
