# Standard library imports
import os
import subprocess
import logging

# Third party imports
from gi.repository import GLib
from pydbus import SystemBus
import yaml

# Local application imports
import lib.utils

# Callback then runs when the speakler connects/disconnects
def on_state_change(sender, message, other):
    # sender <-- string
    # message <-- dictionary with properties that changed and values
    # other <-- list (empty in this app)
    if sender == 'org.bluez.Device1':
        # check how many instance of radio app are running
        radios.refresh() 
        if message['Connected']:
            logging.debug("Speaker connection detected.")
            if radios.count == 0:
                subprocess.call([radio_start_script])
            elif radios.count >1:
                radios.leaveOne
        else:
            logging.debug("Speaker disconnection detected.")
            if radios.count > 0:
                radios.killAll

# Read the config file, set up logging
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'radio_config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.safe_load(ymlfile)
    logging.basicConfig(level=CONFIG["log_level"])
    logging.info("Radio Manager has started.")
# Setup Management of Pianobar
radios = lib.utils.findProcByName("Pianobar")
radio_start_script = CONFIG["radio_start_script"]


# Subscribe to dbus signal and start loop
bus = SystemBus()
speaker = bus.get('org.bluez',
                  '/org/bluez/hci0/dev_' + 
                  CONFIG["speaker_address"].replace(":", "_"))

speaker.onPropertiesChanged = on_state_change
loop = GLib.MainLoop()
loop.run() # blocks until callback comes in
