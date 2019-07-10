Internet Radio
==============
This application sets up a Pandora client on a headless Raspberry Pi with a bluetooth speaker.  Streaming is provided by the terminal Pandora client *pianobar*. Pianobar will ignore adds even on a free Pandora account. The app is designed such that music will automatically start when the speaker is turned on and streaming will stop when the speaker is turned off.  Your music choices are determined by the settings in the *pianobar* *config* file. Further interaction with the pi is not required.  However, you can optionally log in via ssh and change stations, +/- songs, add new stations etc.

Setting up the Raspberry Pi
===========================
*Note: The first 3 steps listed below are standard for setting up a headless Raspberry Pi and are not specific to this project.  A more detailed explanation is available at https://www.raspberrypi.org/documentation/configuration/wireless/headless.md*

1. Burn Raspbian image to sd card
2. Create ssh file and place it in the boot folder on the sd card.
3. If using WiFi create a wpa_supplicant.conf file and place it on the boot folder on the sd card.
4. Boot Pi and connect over ssh using putty or the terminal application of your choice.
5. `$sudo raspi-config` to change password, set time zone, keyboard layout etc.
6. `$sudo apt-get update && sudo apt-get upgrade -y`
7. `$sudo apt-get install screen -y`
8. `$sudo apt-get install pianobar -y`
9. `$sudo apt-get install bluez-tools -y`
10. `$git clone https://github.com/bg1000/InternetRadio.git`

*Note: The above step will create the directectory internet_radio under the directory you run the command from and copy the files from this repository into it.  The directions below assume you have run this command from /home/pi and therefore created the directory /home/pi/internet_radio.*

Setting up Bluetooth
====================

*Note: 0D:F9:82:90:0A:4D is used wherever a device_id/MAC address is used in a command below.  You should substitute the address of your speaker which you will obtain in step # 2 below.*

1. `$ bluetoothctl`
2. `# scan on` (to get the speaker Device id/Mac Address) - will look something like "[NEW] Device 0D:F9:82:90:0A:4D Oontz Angle"
3. `# pair 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
4. `# trust 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
5. `# connect 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
6. `# quit`
7. Speaker may play helpful tone when it connects. Test to make sure speaker automatically connects by turning off and back on. If your speaker does not play a connected tone you can check its status with `$ bt-device -i 0D:F9:82:90:0A:4D`. Look for either *Connected: 0* or *Connected: 1* near the bottom of the output. If your speaker does not automatically connect when turned on you may have to script this.  You can an idea of how to do this from *autoconnect.sh*.
8. With the speaker connected test it with `$ aplay -D bluealsa:DEV=0D:F9:82:90:0A:4D,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav` or `$ bash speaker_test.sh` - You should hear voice from speaker say "Front. Center."
9. *Note: further details on this step can be found at https://alsa.opensrc.org/Asoundrc*. To make your speaker the default audio device: `$ sudo cp asound.conf /etc/asound.conf` - there are 4 things in the file that need to be customized with an editor (e.g. - `$ sudo nano /etc/asound.conf`):
  - the name x 2
  - the description
  - the device id (MAC address) of the speaker
10. `$ sudo reboot`
11. After logging back in connect the speaker and test again without specifying the device i.e. -  `$ aplay /usr/share/sounds/alsa/Front_Center.wav` -- sound should play as before.

Setting up Pianobar
===================
*Note: Additional information on pianobar is availagel here - https://wiki.archlinux.org/index.php/Pianobar*
1. Setup pianobar config:
  - ` $ cd ~`
  - ` /home/pi$ mkdir .config`
  - ` /home/pi$ cd .config`
  - ` /home/pi/.config$ mkdir pianobar`
  - `/home/pi/.config$ cp /home/pi/internet_radio/config /home/pi/.config/pianobar/config`
  - `$ nano /home/pi/.config/pianobar/config` - modify the username and password to the ones associated with your Pandora account.  You can also change any other options in the file.
2. Start the app from the command line with `$ pianobar`
3. If you would like to change the default station type "s".  You will see a numbered list of configured stations setup on your account with a prompt to enter a station number. Enter the desired station number.  Pianobar will change the station and reply with a message similar to this: *Station "Queen Radio" (303915622719377191)*. Edit the config file as shown in step 1 above. Edit the *autostart_station* line and change the station id number i.e. - `autostart_station = 303915622719377191`. The next time pianobar starts it will automatically start this station.
4. To run in screen: `$ screen -d -m pianobar`
5. To find screen `$ screen -list`
6. To kill screen `$ kill PID` (use PID from -list)
7. To switch to screen: `$screen -r PID` (not required but useful to change stations, + or - a particular song, etc.)

Setting up radio_manager.py
===========================

1. To check the speaker status: `$ bt-device -i 0D:F9:82:90:0A:4D`.  Look for *Connected: 0* or *Connected: 1* near the bottom of the output.
2. radio_manager.py polls this connection status and starts and stops pianobar (in a detached screen) accordingly.
3. To setup radio_manager `nano /home/pi/internet_radio/radio_config.yaml`.  Change the speaker address and polling time to meet your needs.
4. radio_manager.py uses the following python libraries that you will need to install using pip if they are not already installed:
    - `pip3 install psutil`
    - `pip3 install PyYAML`
5. To run interactively `$ python3 /home/pi/internet_radio/radio_manager.py`
6. To set this up as a service the file */home/pi/internet_radio/radio_manager@pi.srevice* will be used.  The file already contains a know working setup for running radio_manager.py as a service and no changes should be required.
7. To setup: `$ sudo bash /home/pi/internet_radio/autostart_systemd.sh`. The radio_manager application will now start as a service on the next reboot.  It will log to */var/log/syslog*
8. To start the service without rebooting: `$sudo systemctl start radio_manager@pi`

Final Test
==========

Turn on the speaker.  It should automatically connect. Once the speaker is connected pianobar should start automatically and you should hear your favorite Pandora station. When you are done, simply turn off the speaker.  The radio_manager application will automatically stop pianobar.


