DATADIR			= data/db.json
LAUNCHSCRIPT	= src/launch.py
SEMS			= fa16 su16 sp16 fa15 sp15 fa14 test  # Change this to exclude semesters
LOGIN			= .login

default:
	python -i $(LAUNCHSCRIPT) realtime test --path $(DATADIR) --login $(LOGIN)

scrub-all:
	python -i $(LAUNCHSCRIPT) scrubber test --path $(DATADIR) --login $(LOGIN)

scrub:
	python -i $(LAUNCHSCRIPT) scrubber test --path $(DATADIR) --sems $(SEMS) --login $(LOGIN)

test:
	python
