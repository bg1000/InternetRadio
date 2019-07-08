#!/bin/sh
if [ -z "$STY" ]; then exec screen -dm -S Pandora /bin/bash "$0"; fi
pianobar
