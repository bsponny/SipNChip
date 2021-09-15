# SipNChip

# What this project uses

This application consists of a website built using Django, a full stack web development framework for Python. As such, this project will follow the default organization standards of a Django project, and will follow the default naming and style conventions for Python, PEP-8. Other tools that are used in this project include HTML and JavaScript, which are used to build the webpages themselves. The setup for this project simply consists of a new Django project in an empty folder.

# Version control procedures

This project uses Git for version control, and is hosted at https://github.com/bsponny/SipNChip.git. Individual features of the application will be worked on in their own branches, and merged to the MASTER branch after review by the development team.

# Buid instructions

The website can be launched by running `python manage.py runserver` from the command line in the Django project, then launching the website in a web browser from a device connected to the same network as the server.

# Unit testing instructions

Unit tests will be written using Python's built-in `unittest` library. Any tests that require an external file will be placed in a dedicated folder for unit tests somewhere in the project.

# System testing instructions

The following procedure will be used for system testing:
	1. Website is run from the Django server
	2. One user logs into the website as a manager
	3. Another three users create new player accounts from the public account creation page
	4. Manager creates tournament which players then join
	5. Players input scores to simulate playing the tournament
	6. Players submit scores to the leaderboard and receive cash prizes
	7. Manager switches one player account to bartender, and another player account to sponsor
	8. All users add $1000 to their account
	9. Manager creates another tournament
	10. Sponsor offers to sponsor tournament
	11. Player signs up for tournament
	12. Player places a drink order using the application
	13. Bartender marks the order as complete when received
	14. Player inputs scores to finish tournament
	15. Sponsor requests a tournament using the request form
	16. Player signs up for tournament
	17. Player places a drink order, then cancels it
	18. Player inputs scores to finish tournament
	19. All users log off, server is shut down