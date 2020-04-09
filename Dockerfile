#
# options to look at 
# arm32v7/debian
# arm32v7/ubuntu
# maybe there is a raspbian image?
#
# Python Base Image from https://hub.docker.com/r/arm32v7/python/
# 
 FROM arm32v7/python:3.8.1-buster
# FROM arm32v7/debian:buster

# update the list of packages
RUN apt-get update

# add required packages
RUN apt-get install screen pianobar bluez-tools -y

# Download InternetRadio app
RUN git clone https://github.com/bg1000/InternetRadio.git

RUN mkdir .config
RUN mkdir ./config/pianobar/
RUN cp ./InternetRadio/config ./config/pianobar/config

# Intall required python modules 
RUN pip3 install --no-cache-dir -r ./InternetRadio/requirements.txt

# Run GarageQTPi
CMD ["python3", "./InternetRadio/radio_manager.py"]
