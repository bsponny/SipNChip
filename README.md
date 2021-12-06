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

## System testing instructions

The server comes pre-loaded with an administrator account with the username 'admin' and the password 'SipNChip'. This account has all permissions on the website, including setting the type of other users. This should allow you to create test accounts, set them to any user type other than administrator, and verify that all features of the website function properly.  

The following procedure should verify all immediate functionality of the application is correct:  

1. Verify that user account type access restrictions are functional.
	1. Create a player account using the public registration page, then login with that account.
	2. Attempt to access `localhost:8000/userType` from the address bar; the attempt should fail, reloading the home page. This is only a basic example that should verify the system of access restriction works; if there are any other functions you want to verify are properly secured, you may do so now.
2. Verify that tournaments are properly implemented.
	1. Login with the admin account, then navigate to the Create Tournament page.
	2. Attempt to create a tournament on a previous day; the attempt should fail and display an error message.
	3. Create 2 tournaments for any day including or after today.
	4. Navigate to the Remove Tournaments page, then delete 1 tournament.
	5. Navigate to the View Tournaments page, then sign up for the tournament you created.
	6. Navigate to the View Tournaments Registered For page, then start playing through the tournament you just registered for.
	7. Attempt to input a value for hole 1 that is not between 1 and 5. The attempt should fail and display an error message.
	8. Attempt to navigate to the next hole *without* submitting a score first. The attempt should fail with an error message.
	9. Play through the tournament by submitting valid scores for all 18 holes. Once the 18th hole is submitted, the View Scores button should become visible.
	10. After navigating to the scorecard summary page with the View Scores button, submit your scores to the leaderboard.
3. Verify that sponsor functionality is properly implemented.
	1. Create a sponsor account by setting the player account to sponsor with the admin account, then log in with that account.
	2. After logging in with your account, navigate to the Sponsor Tournament page and attempt to sponsor the existing tournament. This attempt should fail and redirect you to the Add Money to Your Account page. Add $500 to your account now.
	3. Navigate back to the Sponsor Tournament page and sponsor the existing tournament, then unsponsor it and responsor it again.
	4. Navigate to the Request Tournament page and attempt to request a tournament on a previous date. This attempt should fail and display an error message.
	5. Attempt to request a tournament on a valid date. Assuming you have no money in your account after step 3.iii, the attempt should fail and redirect you again to the Add Money to Your Account page. Add another $500 to your account now.
	6. Navigate back to the Request Tournament page and request a tournament on a valid date.
	7. Navigate to the View Sponsor Requests page and deny the request you just made.
	8. Navigate back to the Request Tournament page and request another tournament, then navigate back to the View Sponsor Requests page and approve the request.
	9. Navigate to the View Tournaments page to verify the requested tournament was created.
4. Verify that drink ordering is properly implemented.
	1. Using the admin account, set the sponsor account type to bartender, then login as the bartender.
	2. Navigate to the Add Money to Your Account page, then add $100 to your account.
	3. Navigate to the Order Drinks page, then attempt to place an order totalling over your current balance of $100. This attempt should fail and redirect you to the Add Money to Your Account page. You may add more money to your account if you wish.
	4. Navigate to the Order Drinks page and place an order that you can afford. Navigate back home and verify your balance has changed.
	5. Navigate to the View Your Current Drink Orders page (not the View Drink Orders page) and cancel your order. Navigate back to the home page and verify your balance has once again changed back to its original value.
	6. Navigate back to the Order Drinks page and place another order you can afford.
	7. Navigate to the View Drink Orders page (not the View Your Current Drink Orders page) and mark the order as complete. The order should be removed.
	8. Navigate to the Edit Drink Menu page.
	9. Click Add Drink, then add a drink.
	10. Click Edit on the drink you just added, edit it, then save the changes.
	11. Remove the drink you just edited.
	
Assuming you have reached the end of this procedure without encountering any errors or deviations from the procedure, all immediate functionality of the application should be working correctly. The Archived Tournaments page should update with your created tournament once its date passes, and the account that played the tournament should receive $100. Congratulations! We hope you enjoy this application.