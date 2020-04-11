#import os
import subprocess
import time
import yaml
import os
import utils
import sys
from subprocess import CalledProcessError
print ("Radio Manager Starting")

#
# Set up
#

# allow this looping app to receive termination signals
killer = utils.GracefulKiller()
# Setup Management of Pianobar
radios = utils.findProcByName("Pianobar")
radio_start_script = str(os.path.join(os.path.abspath(os.path.dirname(__file__)))) + "/run_pianobar.sh"

# open the config file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'radio_config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.safe_load(ymlfile)
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
#        print ("Checking to see if speaker is connected")

        try:
            result = subprocess.check_output(['bt-device', '-i', CONFIG['speaker_address']]).decode(sys.stdout.encoding)         
            out = result.split()
            for st in out:
                if  ("Connected" in st):
                    ind = out.index(st) + 1
                    if "0" in out[ind]:
                        speaker_connected = False
                        #print("Speaker not connected")
                    elif "1" in out[ind]:
                        speaker_connected = True
                        print("Speaker connected")
                    else:
                        speaker_connected = None
                        print("Error - Can't Determine if speaker is connected")
            if (not speaker_connected and radios.count > 0):
                radios.killAll()
            elif (speaker_connected and radios.count == 0):
                subprocess.call([radio_start_script])
            elif (speaker_connected and radios.count > 1):
                radios.leaveOne()
        except CalledProcessError:
            print("Unable to call bt_device")
        if killer.kill_now:
          break

        time.sleep(CONFIG['sleep_seconds']) 
        radios.refresh() # refresh PID list for next iteration


