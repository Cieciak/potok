#! /bin/bash
if [ -d .venv ]; then
  echo "Python venv already exists"
else
  python3 -m venv .venv
fi

source ".venv/bin/activate"
pip3 install -r requirements.txt

if [ "$1" == "dev" ]; then
  echo "Developer env"
  pip3 install -e .
fi