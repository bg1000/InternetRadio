#! /bin/bash
git clone https://github.com/bg1000/InternetRadio
cd InternetRadio
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
deactivate
