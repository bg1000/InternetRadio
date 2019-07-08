#import os
import time
import yaml
import os
import bluetooth
import utils
print ("Radio Manager Starting")

#
# Set up
#

# allow this looping app to receive termination signals
killer = utils.GracefulKiller()
# Setup Management of Pianobar
radios = utils.findProcByName("Pianobar")


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
        print ("Scanning for bluetooth devices")
        nearby_devices = bluetooth.discover_devices(lookup_names=False, duration=30, flush_cache=True, lookup_class=False)
        print("found %d devices" % len(nearby_devices))

        for addr in nearby_devices:
            # print("  %s - %s" % (addr, name))
            print("  %s" % str(addr))
        # speaker address is CONFIG['speaker_address']
        # check for Pandora app already running
        # check for speaker connected
        # start or stop radio and make number of Pandora instances correct
        if killer.kill_now:
          break

        time.sleep(CONFIG['sleep_seconds']) 
        radios.refresh() # refresh PID list for next iteration


