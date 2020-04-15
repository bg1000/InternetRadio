#
# options to look at 
# For RPI Zero-W https://hub.docker.com/r/arm32v6/python (apline)
#
# Python Base Image from https://hub.docker.com/r/arm32v7/python/
# 
 FROM arm32v7/python:3.8.1-buster
# FROM arm32v7/debian:buster

# update the list of packages & add required packages
RUN apt-get update && apt-get install -y screen pianobar bluez-tools bluez bluetooth usbutils

# Download InternetRadio app
# skip this for now and use local copy so we can make changes
# RUN git clone https://github.com/bg1000/InternetRadio.git

# RUN mkdir .config
# RUN cd .config
# RUN mkdir ./.config/pianobar
# RUN cp * ./.config/pianobar/config

# remove this when git clone is added back
RUN mkdir .InternetRadio
COPY requirements.txt ./InternetRadio/requirements.txt

# Intall required python modules 
RUN pip3 install --no-cache-dir -r ./InternetRadio/requirements.txt

# Run GarageQTPi
CMD ["/bin/sh", "/config/container_start.sh"]
