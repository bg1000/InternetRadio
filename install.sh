#! /bin/bash
mkdir InternetRadio
cd InternetRadio
git clone https://github.com/bg1000/InternetRadio
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
deactivate
