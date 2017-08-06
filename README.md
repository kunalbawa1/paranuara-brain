# Paranuara-brain
Brain server to serve the needs of Planet Paranuara using Django.

## Challenge
The government from Paranuara has provided two json files (located at resource folder) that contains the information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet. The system must provide the following REST API calls:

1. /paranuara/employees?name=COMPANY_NAME - The API needs to return all the employees for the provided company.
2. /paranuara/friends?p1=USERNAME&p2=USERNAME - Given 2 person's username which in this will be the email, should provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
3. /paranuara/person?username=USERNAME - Given 1 person's username, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}

## Installation
The application could be installed and run by performing the following steps:
- cd /path/to/your/workspace
- git clone https://github.com/kunalbawa1/paranuara-brain.git projectname && cd projectname
- ./run.sh (optional arguments: -h for the help section,
                                -n to skip pip installations & db initialisation if already done once and virtualenv is activated using 'source env/bin/activate''.)
- After this any requests can be to the server (running at 127.0.0.1:7000) for example:
  - http://0.0.0.0:7000/paranuara/employees?name=APPLICA
  - http://0.0.0.0:7000/paranuara/friends?p1=carmellalambert@earthmark.com&p2=deckermckenzie@earthmark.com
  - http://0.0.0.0:7000/paranuara/person?username=carmellalambert@earthmark.com

The script run.sh is responsible for:
 - Installing and activating virtual environment.
 - Installing pip packages defined in the requirements.txt
 - Setting up that database which involves create a mysql account, migrating the database and uploading the data from the resources in the newly created db.
 - Lastly, starting the django HTTP server on port 7000.

## Project Structure

```GAP
projectname
   |__ run.sh               # Install dependencies and start django server.
   |__ db_setup.sh          # Setup database credentials and run django migrations
   |__ requirements.txt
   |__ brain                # All application code in this directory
   |   |__ brain
   |   |   |__ __init__.py
   |   |   |__ settings.py
   |   |   |__ url.py
   |   |   |__ wsgi.py
   |   |
   |   |__ paranuara
   |   |   |__ migrations  # Migrations that are responsible for creating tables and also uploading data from resources.
   |   |   |__ __init__.py
   |   |   |__ admin.py
   |   |   |__ models.py
   |   |   |__ views.py
   |   |
   |   |__ lib
   |   |   |__ __init__.py
   |   |   |__ person.py
   |   |
   |   |__ wstypes
   |   |   |__ __init__.py
   |   |   |__ error.py    # Response type to be returned in case an error is raised.
   |   |   |__ person.py   # Response type to be returned when getting Person object from db.
   |   |   |__ wslist.py   # Response type to be returned when getting list of items.
   |   |
   |   |__ manage.py       # A command-line utility that lets you interact with the Brain server in various ways.
   |   |__ __init__.py

## Additional Features
Django Admin Webpage - Website that allows you to add, change or delete data regarding person, company etc.

In order to use it an admin account needs to be created first, please perform the following steps to do so:
1. cd /path/to/your/project
2. source env/bin/activate (before doing this step please sure that ./run.sh is run at-least one else dependencies won't be installed)
3. python brain/manage.py createsuperuser (Please provide the desired credentials when prompted for)

Lastly running the server:
1. ./run.sh -n (make sure -n is provided this time otherwise db will be wiped out and hence it won't have details of the superuser account.)
2. Access the admin page using URL - http://0.0.0.0:7000/admin/


