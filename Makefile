DATADIR			= data/db.json
LAUNCHSCRIPT	= src/launch.py
SEMS			= fa16 su16 sp16 fa15 sp15 fa14 test  # Change this to exclude semesters
LOGIN			= .login

default: scrape

real:
	python -i $(LAUNCHSCRIPT) realtime test --path $(DATADIR) --login $(LOGIN)

scrape-all:
	python -i $(LAUNCHSCRIPT) scraper test --path $(DATADIR) --login $(LOGIN)

scrape:
	python -i $(LAUNCHSCRIPT) scraper test --path $(DATADIR) --sems $(SEMS) --login $(LOGIN)

test:
	python

clean:
	find . -type f -name '*.pyc' -delete
