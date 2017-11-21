DATADIR			= data/db.json
LAUNCHSCRIPT	= src/launch.py
SEMS			= fa16 su16 sp16 fa15 sp15 fa14 test  # Change this to exclude semesters
LOGIN			= .login

default: test

real:
	python $(LAUNCHSCRIPT) realtime test --path $(DATADIR) --login $(LOGIN)

scrape-all:
	python $(LAUNCHSCRIPT) scraper test --path $(DATADIR) --login $(LOGIN)

scrape:
	python $(LAUNCHSCRIPT) scraper test --path $(DATADIR) --sems $(SEMS) --login $(LOGIN)

test:
	python $(LAUNCHSCRIPT) oracle test --path $(DATADIR)

clean:
	find . -type f -name '*.pyc' -delete
