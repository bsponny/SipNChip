# SipNChip

## What this project uses (tool stack)

This application consists of a website built using Django, a full stack web development framework for Python. Other tools that are used in this project include HTML and (possibly) JavaScript, which are used to build the webpages themselves. The setup for this project simply consists of a Django project in a dedicated folder, `SipNChip`.

## Tool stack and setup

The tool stack, as previously mentioned, is Django (Python), HTML, and JavaScript. To set up for this project, each team member has downloaded Python on their computer and installed the Django package using Pip: `bash $ python -m pip install Django`. Each team member must also have a text editor capable of editing Python, HTML, and JavaScript files.

## Tool stack setup

Each member of the development team must download Python 3.7 or greater to their local computer, then install the Django package. The best way to install Django is to use Pip:  
`bash $ python -m pip install Django`  
Each team member must also use a text editor (or editors) that can edit Python, HTML, and JavaScript.  

## Organization procedures

The Django project will be automatically set up in the `SipNChip` folder, and all application files will be organized according to Django's required structure. All other resources for the project can be found in the `docs` folder.

## Naming scheme

This project will follow the naming schemes required by Django, as well as adhereing to the style conventions of PEP-8.

## Version control procedures

This project uses Git for version control, and is hosted at https://github.com/bsponny/SipNChip.git. Each member of the team will clone this repository to their personal computers. During the development phase of this project, each member will submit pull requests when making changes to the repository, which must be approved by the team. In addition, each feature of the app should have its own branch for development that members work on and merge into MASTER when complete.

## Build instructions

Install Python to your computer, then install Django if you have not done so already.  
`bash $ python -m pip install Django`  

Clone the project from GitHub to your local repository.  
`bash $ git clone https://github.com/bsponny/SipNChip.git <your-repository>` 

Open a command line such as Bash, then navigate to the `SipNChip` directory.  
`bash $ cd <your-repository>/SipNChip

Apply all migrations to the project, then create a superuser.  
`bash $ python manage.py migrate`
`bash $ python manage.py createsuperuser`  
  

Run the server, then launch the app from localhost:8000 in your web browser.  
`bash $ python manage.py runserver`  

## Unit testing instructions

Unit tests will be written using Python's built-in `unittest` library. A file called `unittests.py`, which contains all necessary unit tests for this project, can be found in the `SipNChipApp` folder of the project.

## System testing instructions

The superuser account that you made when building the project should allow you full administrator access to the database and its contents, which you can use to verify that the website functions properly.