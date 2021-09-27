# SipNChip

## What this project uses

This application consists of a website built using Django, a full stack web development framework for Python. Other tools that are used in this project include HTML and JavaScript, which are used to build the webpages themselves. The setup for this project simply consists of a Django project in a dedicated folder, `SipNChip`.

## Organization procedures

The Django project will be automatically set up in the `SipNChip` folder, and all application files will be organized according to Django's required structure. All other resources for the project can be found in the `docs` folder.

## Naming scheme

This project will follow the naming schemes required by Django, as well as adhereing to the style conventions of PEP-8.

## Version control procedures

This project uses Git for version control, and is hosted at https://github.com/bsponny/SipNChip.git. Each member of the team will clone this repository to their personal computers and submit pull requests when making changes to the repository, which must be approved by the team. In addition, each feature of the app should have its own branch for development that members work on and merge into MASTER when complete.

## Build instructions

Clone the project from GitHub to your local repository.  
`bash $ git clone https://github.com/bsponny/SipNChip.git <your-repository>`  

Create a virtual environment in Bash, then begin setting up the Django server.  
`bash $ virtualenv --no-site-packages`  
`bash $ python manage.py migrate` 

Create an admin account for system testing purposes, then migrate again.  
`bash $ python manage.py createsuperuser` 
`bash $ python manage.py makemigrations SipNChip`  
`bash $ python manage.py migrate`  

Run the server, then launch the app from localhost:8000 in your web browser.  
`bash $ python manage.py runserver`  

## Unit testing instructions

Unit tests will be written using Python's built-in `unittest` library. A file called `unittests.py`, which contains all necessary unit tests for this project, can be found in the `SipNChip` folder.

## System testing instructions

Once the server has been launched, log into the app with username: owner and password: hunter2. This account should have all permissions, allowing for complete system testing.