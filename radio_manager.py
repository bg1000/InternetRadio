#import os
import subprocess
import time
import yaml
import os
import lib.utils
import sys
from subprocess import CalledProcessError
if lib.utils.add_package_path("bluetool"):
    from bluetool import Bluetooth
else:
    print("Can't find an installed version of bluetool. Exiting")
    sys.exit(1)
print ("Radio Manager Starting")

#
# Set up
#

# allow this looping app to receive termination signals
killer = lib.utils.GracefulKiller()
# Setup Management of Pianobar
radios = lib.utils.findProcByName("Pianobar")
radio_start_script = str(os.path.join(os.path.abspath(os.path.dirname(__file__)))) + "/run_pianobar.sh"

# open the config file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'radio_config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.safe_load(ymlfile)

bluetooth = Bluetooth()

#
# End Setup
#

#
# Main Loop
#
if __name__ == "__main__":
    while True:
        if killer.kill_now:
            break
        print ("Checking to see if speaker is connected")

        devices = bluetooth.get_connected_devices()
        speaker_connected = False
        if devices:
            for device in devices:
                if device["Address"] == CONFIG['speaker_address']:
                    speaker_connected = True
                    break
        if (not speaker_connected and radios.count > 0):
            radios.killAll()
        elif (speaker_connected and radios.count == 0):
            subprocess.call([radio_start_script])
        elif (speaker_connected and radios.count > 1):
            radios.leaveOne()
        if killer.kill_now:
          break

        time.sleep(CONFIG['sleep_seconds']) 
        radios.refresh() # refresh PID list for next iteration


