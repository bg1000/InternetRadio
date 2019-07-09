Setting up the Raspberry Pi
===========================

- Burn Raspbian image to sd card
- Create ssh file on card
- If using WiFi create ... file
- Boot Pi
- $sudo raspi-config to change password, set time zone, keyboard layout etc.
- $sudo apt-get update && sudo apt-get upgrade -y
- $sudo apt-get install screen -y
- $sudo apt-get install pianobar -y
- $sudo apt-get install bluez-utils -y --> not sure if this is correct

Setting up Bluetooth
====================

- $bluetoothctl
- \# scan on (to get the speaker Device id/Mac Address) - will look something like "[NEW] Device 0D:F9:82:90:0A:4D Oontz Angle"
- \# pair 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
- \# trust 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
- \# connect 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
- \# quit
- Speaker may play helpful tone when it connects. Test to make sure speaker automatically connects by turning off and back on.
- With speaker connected test it with aplay -D bluealsa:DEV=0D:F9:82:90:0A:4D,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav or speaker_test.sh - Speaker should play wave.
- Move asound.conf to /etc/asound.conf - there are 4 things in the file that need to be customized: 
  - the name x 2
  - the description
  - the device id (MAC address) of the speaker
- $sudo reboot
- After logging back in connect the speaker and test again with aplay /usr/share/sounds/alsa/Front_Center.wav -- sound should play as before.

Setting up Pianobar
===================

- Move config  to /home/pi/.config/pianobar/config - add the correct Pandora username and password to the file and change whatever other options as desired.
- you should be able to start the app with $ pianobar
- to run in screen: $ screen -d -m pianobar
- to find screen $ screen -list
- to kill screen $ kill PID (use PID from -list)
- to switch to screen: $screen -r PID

Setting up radio_manager.py
===========================

- to check the speaker status: $ bt-device -i 0D:F9:82:90:0A:4D.  This will show a few different things.  Near the bottom it will show "Connected: 0" or "Connect: 1"
- radio_manager.py polls this connection status and starts and stops pianobar (in a detached screen) accordingly.
- to setup radio_manager edit /home/pi/internet_radio/radio_config.yaml.  Change the speaker address and polling time to meet your needs.
- radio_manager.py uses a number of python libraries that you will need to install using pip if they are not already installed:
    - pip3 install psutil
    - pip3 install
    - pip3 install
- to run interactively $ python3 /home/pi/internet_radio/radio_manager.py
- to set this up as a service the file /home/pi/internet_radio/radio_manager@pi.srevice will be used.  It should already be setup correctly buy you can modify it if desired.
- to setup: $ sudo bash /home/pi/internet_radio/autostart_systemd.sh. radio_manager will now start as a service on reboot.  It will log to /var/log/syslog
- to start the service without rebooting: $sudo systemctl start radio_manager@pi


