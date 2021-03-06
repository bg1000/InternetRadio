Internet Radio
==============
This application sets up a Pandora client on a headless Raspberry Pi with a bluetooth speaker.  Streaming is provided by the terminal Pandora client *pianobar*. *Pianobar* will ignore ads even on a free Pandora account. The app is designed such that music will automatically start when the speaker is turned on and streaming will stop when the speaker is turned off.  Your music choices are determined by the settings in the *pianobar* *config* file. Further interaction with the pi is not required.  However, you can optionally log in via ssh and change stations, +/- songs, add new stations etc.

Setting up the Raspberry Pi
===========================
*Notes: 
- The first 3 steps listed below are standard for setting up a headless Raspberry Pi and are not specific to this project.  A more detailed explanation is available at https://www.raspberrypi.org/documentation/configuration/wireless/headless.md*
- These instructions and the scripts all assume you are setting this up to run as the pi user and you are starting in the pi home directory (/home/pi). The application itself will be installed in the /home/pi/InternetRadio directory in a python virtual environment.

1. Burn Raspbian image to sd card. These instructions are for Raspbian lite. If you install another version you may already have some of these packages.
2. Create ssh file and place it in the boot folder on the sd card.
3. If using WiFi create a wpa_supplicant.conf file and place it on the boot folder on the sd card.
4. Boot Pi and connect over ssh using putty or the terminal application of your choice.
5. `$sudo raspi-config` to change password, set time zone, keyboard layout etc.
6. `$sudo apt-get update && sudo apt-get upgrade -y`
7. `$sudo apt-get install git screen pianobar bluez-tools bluealsa python3-pip python3-venv libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 -y`
8. `$ bash <(curl -s https://raw.githubusercontent.com/bg1000/InternetRadio/master/install.sh)`
11. `$sudo adduser pi bluetooth`
12. `$sudo reboot`

*Note: The above step will create the directectory InternetRadio under the directory you run the command from and copy the files from this repository into it.  The directions below assume you have run this command from /home/pi and therefore created the directory /home/pi/internet_radio.*

Setting up Bluetooth
====================

*Note: 0D:F9:82:90:0A:4D is used wherever a device_id/MAC address is used in a command below.  You should substitute the address of your speaker which you will obtain in step # 2 below.*

1. `$ sudo bluetoothctl`
2. `# scan on` (to get the speaker Device id/Mac Address) - will look something like "[NEW] Device 0D:F9:82:90:0A:4D Oontz Angle"
3. `# pair 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
4. `# trust 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
5. `# connect 0D:F9:82:90:0A:4D` (shows message that it is attempting and then second message with success or failure).
6. `# quit`
7. Speaker may play helpful tone when it connects. Test to make sure speaker automatically connects by turning off and back on. If your speaker does not play a connected tone you can check its status with `$ bt-device -i 0D:F9:82:90:0A:4D`. Look for either *Connected: 0* or *Connected: 1* near the bottom of the output. If your speaker does not automatically connect when turned on you may have to script this.  You can get an idea of how to do this from *home/pi/internet_radio/autoconnect.sh*.
8. With the speaker connected test it with `$ aplay -D bluealsa:DEV=0D:F9:82:90:0A:4D,PROFILE=a2dp /usr/share/sounds/alsa/Front_Center.wav` or `$ bash speaker_test.sh` - You should hear a voice from speaker say "Front. Center."
9. *Note: further details on this step can be found at https://alsa.opensrc.org/Asoundrc*. To make your speaker the default audio device: `$ sudo cp asound.conf /etc/asound.conf` - there are 4 things in the file that need to be customized with an editor (e.g. - `$ sudo nano /etc/asound.conf`):
   - the name x 2
   - the description
   - the device id (MAC address) of the speaker
10. `$ sudo reboot`
11. After logging back in connect the speaker and test again without specifying the device i.e. -  `$ aplay /usr/share/sounds/alsa/Front_Center.wav` -- sound should play as before.

Setting up Pianobar
===================
*Note: Additional information on pianobar is available here - https://wiki.archlinux.org/index.php/Pianobar*
1. Setup pianobar config:
   - ` $ cd ~`
   - ` /home/pi$ mkdir .config`
   - ` /home/pi$ cd .config`
   - ` /home/pi/.config$ mkdir pianobar`
   - `/home/pi/.config$ cp /home/pi/InternetRadio/config /home/pi/.config/pianobar/config`
   - `$ nano /home/pi/.config/pianobar/config` - modify the username and password to the ones associated with your Pandora account.  You can also change any other options in the file.
2. Start the app from the command line with `$ pianobar`
3. If you would like to change the default station type "s".  You will see a numbered list of configured stations setup on your account with a prompt to enter a station number. Enter the desired station number.  Pianobar will change the station and reply with a message similar to this: *Station "Queen Radio" (303915622719377191)*. Edit the config file as shown in step 1 above. Edit the *autostart_station* line and change the station id number i.e. - `autostart_station = 303915622719377191`. The next time pianobar starts it will automatically start this station.
4. To run in screen: `$ screen -d -m pianobar`
5. To find screen `$ screen -list`
6. To kill screen `$ kill PID` (use PID from -list)
7. To switch to screen: `$screen -r PID` (not required but useful to change stations, + or - a particular song, etc.)

Setting up radio_manager.py
===========================

1. To check the speaker status: `$ bt-device -i 0D:F9:82:90:0A:4D`.  Look for *Connected: 0* or *Connected: 1* near the bottom of the output. radio_manager subscribes to a dbus signal that notifies it when this property changes.  When it changes to Connected: 1 it starts the radio.  When it changes to Connect: 0 it stops the radio. If music doesn't start when you turn on your speaker, verify it is connecting with the command shown above.
3. To setup radio_manager `nano /home/pi/internet_radio/radio_config.yaml`.  Change the speaker address and polling time to meet your needs.
4. To run interactively `$ python3 /home/pi/internet_radio/radio_manager.py`
5. To set this up as a service the file */home/pi/InternetRadio/radio_manager@pi.srevice* will be used.  The file already contains a known working setup for running radio_manager.py as a service and no changes should be required.
6. To setup: `$ sudo bash /home/pi/InternetRadio/autostart_systemd.sh`. The radio_manager application will now start as a service on the next reboot.  It will log to */var/log/syslog*
7. To start the service without rebooting: `$sudo systemctl start radio_manager@pi`

Final Test
==========

Turn on the speaker.  It should automatically connect. Once the speaker is connected pianobar should start automatically and you should hear your favorite Pandora station. When you are done, simply turn off the speaker.  The radio_manager application will automatically stop pianobar.

# TroubleShooting
1) If you are having trouble getting bluetooth working on the pi you may find this blog post and the ones it links to helpful. In addition to general setup help, the author explores some of the differences in different versions of Raspbian, alsa and blue-alsa which may be helpful if you are not running current versions.

https://sigmdel.ca/michel/ha/rpi/bluetooth_n_buster_01_en.html

This stack exchange post, while for the raspberry pi zero specifically may also be usefuil - https://raspberrypi.stackexchange.com/questions/90267/how-to-stream-sound-to-a-bluetooth-device-from-a-raspberry-pi-zero

2)The current version of asound.conf in the repository works with Raspbian buster.  There is an older version in the history that worked with Raspbian stretch.rns

3) If aplay returns `open error: No such device` double check to make sure the speaker is paired, on, and connected. You can also try modifing the bluettoth service file as follows:
`sudo nano /etc/systemd/system/bluetooth.target.wants/bluetooth .service`
`ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap --plugin=a2dp`
`sudo systemctl daemon-reload`
`systemctl restart bluetooth`

4)You can verify the bluetooth connectivity on D-Bus with `busctl tree org.bluez`
5) If the speaker did not actually pair properly it may help to start over by typing `remove 0D:F9:82:90:0A:4D` in bluetoothctl.
