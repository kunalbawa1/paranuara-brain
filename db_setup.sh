#!/bin/bash
# Script to setup db

DB_USERNAME='django_user'
DB_PASSWORD='3wJPnOsu27I3'
DB_NAME='django_db'

# Check we are running bash
if [ -z "$BASH" ]
then
    echo "This needs to run using bash by either running like;"
    echo " ./db_initialise.sh"
    echo " bash db_initialise.sh"
    exit 1
fi

echo "# Initialising DB: "
echo -e "\t DB Username: $DB_USERNAME"
echo -e "\t DB Password: $DB_PASSWORD"
echo -e "\t DB Name: $DB_NAME"

Q1="DROP DATABASE IF EXISTS $DB_NAME; DROP USER IF EXISTS '$DB_USERNAME'@'localhost'; DROP USER IF EXISTS '$DB_USERNAME'@'127.0.0.1';"
Q2="CREATE DATABASE $DB_NAME DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
Q3="CREATE USER '$DB_USERNAME'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
Q4="CREATE USER '$DB_USERNAME'@'127.0.0.1' IDENTIFIED BY '$DB_PASSWORD';"
Q5="GRANT ALL ON $DB_NAME.* TO '$DB_USERNAME'@'localhost';"
Q6="GRANT ALL ON $DB_NAME.* TO '$DB_USERNAME'@'127.0.0.1';"
Q7="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}${Q4}${Q5}${Q6}${Q7}"

mysql -uroot -e "$SQL"
echo "Database successfully initialised!"

# Initialise Django DB
python brain/manage.py migrate


