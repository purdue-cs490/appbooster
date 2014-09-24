# AppBooster

AppBooster Django web console

## Setup

1. Install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation).
2. Run ```virtualenv --no-site-packages ENV```
3. Run ```source ENV/bin/activate```
4. Run ```pip install -r requirements.txt```

## Running

### Local

	export ENVIRONMENT=dev
	./manage.py runserver

### Production

	export ENVIRONMENT=prod
	./manage.py runserver
