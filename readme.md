Setting up the Raspberry Pi
===========================
*Note: The first 3 steps listed below are standard for setting up a headless Raspberry Pi and are not specific to this project.  A more detailed explanation is available at https://www.raspberrypi.org/documentation/configuration/wireless/headless.md*

1. Burn Raspbian image to sd card
2. Create ssh file and place it in the boot folder on the sd card.
3. If using WiFi create a wpa_supplicant.conf file and place it on the boot folder on the sd card.
4. Boot Pi and connect over ssh using putty or the terminal application of your choice.
5. $sudo raspi-config to change password, set time zone, keyboard layout etc.
6. $sudo apt-get update && sudo apt-get upgrade -y
7. $sudo apt-get install screen -y
8. $sudo apt-get install pianobar -y
9. $sudo apt-get install bluez-utils -y --> not sure if this is correct
10. $git clone https://github.com/bg1000/InternetRadio.git

*Note: The above step will create the directectory internet_radio under the directory you run the command from and copy the files from this repository into it.  The directions below assume you have run this command from /home/pi and therefore created the directory /home/pi/internet_radio.*

Setting up Bluetooth
====================

1. $bluetoothctl
2. \# scan on (to get the speaker Device id/Mac Address) - will look something like "[NEW] Device 0D:F9:82:90:0A:4D Oontz Angle"
3. \# pair 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
4. \# trust 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
5. \# connect 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
6. \# quit
7. Speaker may play helpful tone when it connects. Test to make sure speaker automatically connects by turning off and back on.
8. With speaker connected test it with $aplay -D bluealsa:DEV=0D:F9:82:90:0A:4D,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav or speaker_test.sh - Speaker should play wave.
9. To make your speaker the default audio device: move asound.conf to /etc/asound.conf - there are 4 things in the file that need to be customized: 
  - the name x 2
  - the description
  - the device id (MAC address) of the speaker
10. $sudo reboot
11. After logging back in connect the speaker and test again without specifying the device i.e. -  $aplay /usr/share/sounds/alsa/Front_Center.wav -- sound should play as before.

Setting up Pianobar
===================

1. Move config  to /home/pi/.config/pianobar/config - add the correct Pandora username and password to the file and change whatever other options as desired.
2. you should be able to start the app with $ pianobar
3. to run in screen: $ screen -d -m pianobar
4. to find screen $ screen -list
5. to kill screen $ kill PID (use PID from -list)
6. to switch to screen: $screen -r PID (not required but useful to change stations, + or - a particular song, etc.)

Setting up radio_manager.py
===========================

1. to check the speaker status: $ bt-device -i 0D:F9:82:90:0A:4D.  This will show a few different things.  Near the bottom it will show "Connected: 0" or "Connected: 1"
2. radio_manager.py polls this connection status and starts and stops pianobar (in a detached screen) accordingly.
3. to setup radio_manager edit /home/pi/internet_radio/radio_config.yaml.  Change the speaker address and polling time to meet your needs.
4. radio_manager.py uses the following python libraries that you will need to install using pip if they are not already installed:
    - pip3 install psutil
    - pip3 install PyYAML
5. to run interactively $ python3 /home/pi/internet_radio/radio_manager.py
6. to set this up as a service the file /home/pi/internet_radio/radio_manager@pi.srevice will be used.  It should already be setup correctly but you can modify it if you understand how it works and would like to make changes.
7. to setup: $ sudo bash /home/pi/internet_radio/autostart_systemd.sh. radio_manager will now start as a service on next reboot.  It will log to /var/log/syslog
8. to start the service without rebooting: $sudo systemctl start radio_manager@pi

Final Test
==========

Turn on the speaker.  It should automatically connect. Once the speaker is connected pianobar should start automatically and you should hear your favorite Pandora station. When you are done, simply turn off the speaker.  radio_manager will automatically stop pianobar.


