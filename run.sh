#!/bin/bash
# Script to setup and run the server

# Port on which the brain server will run
PORT=7000

switch=${1:-local}
if [ $switch == "-h" ] || [ $switch == "-help" ]
then
    echo -e "Script to setup and run the brain. " \
    "\t\n Add '-n' to skip the db initialisation & package installation." \
    exit 0
fi

if [ ! -d "env" ]
then
    virtualenv env
fi

# If env isn't activated, activate for this shell
if [ -z "$VIRTUAL_ENV" ]
then
    source env/bin/activate
fi

# Install add dependencies & Setup DB
if [ $switch == "-n" ]
then
    echo "Skipping requirements & db initialisation..."
else
    echo "Installing requirements"
    pip install -r requirements.txt

    echo "Initialisation DB"
    bash ./db_setup.sh
fi

echo "Starting server at port $PORT"
python brain/manage.py runserver 0.0.0.0:$PORT