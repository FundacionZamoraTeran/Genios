test:
	nosetests --verbose --with-coverage

run:
	python genios.py

sugar:
	-pkill -9 Xephyr
	sugar-runner --resolution 1200x900
