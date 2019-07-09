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
-  $sudo apt-get install bluez-utils -y --> not sure if this is correct
10) $bluetoothctl
11) # scan on (to get the speaker Device id/Mac Address) - will look something like "[NEW] Device 0D:F9:82:90:0A:4D Oontz Angle"
12) # pair 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
13) # trust 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
14) # connect 0D:F9:82:90:0A:4D (shows message that it is attempting and then second message with success or failure).
15) # quit
16) Speaker may play helpful tone when it connects. Test to make sure speaker automatically connects by turning off and back on.
17) With speaker connected test it with aplay -D bluealsa:DEV=0D:F9:82:90:0A:4D,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav or speaker_test.sh - Speaker should play wave.
18) Move asound.conf to /etc/asound.conf - there are 4 things in the file that need to be customized: 
- the name x 2
- the description
- the device id (MAC address) of the speaker
19) $sudo reboot
20) After logging back in connect the speaker and test again with aplay /usr/share/sounds/alsa/Front_Center.wav -- sound should play as before.
21) Move config  to /home/pi/.config/pianobar/config - add the correct Pandora username and password to the file and change whatever other options as desired.
22) you should be able to start with $ pianobar
23) to run in screen: $ screen -d -m pianobar
24) to find screen $ screen -list
25) to kill screen $ kill PID (use PID from -list)
26) to switch to screen: $screen -r PID 
27) to check the speaker status: $ bt-device -i 0D:F9:82:90:0A:4D.  This will show a few different things.  Near the bottom it will show "Connected: 0" or "C$
28) radio_manager.py polls this connection status and starts and stops pianobar (in a detached screen) accordingly.
29) to setup radio_manager edit /home/pi/internet_radio/radio_config.yaml.  Change the speaker address and polling time to meet your needs.
30) to run interactively $ python3 /home/pi/internet_radio/radio_manager.py
31) to set this up as a service the file /home/pi/internet_radio/radio_manager@pi.srevice will be used.  It should already be setup correctly buy you can mod$
32) to setup: $ sudo bash /home/pi/internet_radio/autostart_systemd.sh. radio_manager will now start as a service on reboot.  It will log to /var/log/syslog
33) to start immediatly: $sudo systemctl start radio_manager@pi


