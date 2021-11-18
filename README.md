# SipNChip

## What this project uses (tool stack)

This application consists of a website built using Django, a full stack web development framework for Python. Specifically, this project uses HTML templates which Django automatically populates with information from a database, allowing for dynamic generation of webpages. The setup for this project simply consists of a Django project in a dedicated folder, `SipNChip`.

## Tool stack setup

Each member of the development team must download Python 3.7 or greater to their local computer, then install the Django package. The best way to install Django is to use Pip:  
`bash $ python -m pip install Django`  
Each team member must also use a text editor (or editors) that can edit Python and HTML.  

## Organization procedures

The Django project will be automatically set up in the `SipNChip` folder, and all application files will be organized according to Django's required structure. All other resources for the project can be found in the `docs` folder.

## Naming scheme

This project will follow the naming schemes required by Django, as well as adhereing to the style conventions of PEP-8.

## Version control procedures

This project uses Git for version control, and is hosted at https://github.com/bsponny/SipNChip.git. Each member of the team will clone this repository to their personal computers. During the development phase of this project, each member will submit pull requests when making changes to the repository, which must be approved by the team. In addition, each feature of the app should have its own branch for development that members work on and merge into MASTER when complete.

## Build instructions

Install Python to your computer, then install Django and other dependent modules if you have not done so already.  
`bash $ python -m pip install Django`  
`bash $ python -m pip install django-crispy-forms`  

Clone the project from GitHub to your local repository.  
`bash $ git clone https://github.com/bsponny/SipNChip.git <your-repository>`  

Open a command line such as Bash, then navigate to the `SipNChip` directory.  
`bash $ cd <your-repository>/SipNChip`  

Apply all migrations to the project 
`bash $ python manage.py migrate`  
 
Run the server, then launch the app from localhost:8000 in your web browser.  
`bash $ python manage.py runserver`  

## Testing procedures

As development of features occurs, each team member is repsonsible for verifying that each feature they develop is capable of all required functionality without causing errors or bugs. For example, as Gavin develops the page for managers to create tournaments, he verifies that the page creates a tournament on the specified date by running the server and using the page to create a tournament, then checking the page with a list of available tournaments to verify that the tournament was created. After a feature is fully developed, the team should pull the changes from the repository and verify that the feature runs properly without breaking anything else on the server.  

## System testing instructions (subject to change)

The server comes pre-loaded with an administrator account with the username 'admin' and the password 'SipNChip'. This account has all permissions on the website, including setting the type of other users. This should allow you to create test accounts, set them to any user type other than administrator, and verify that all features of the website function properly.