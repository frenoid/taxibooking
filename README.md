# Motional Take Home Exercise - Done by Lim Xing Kang Norman

## Taxi booking system

## To Run

Clone the repo
```
git clone https://github.com/frenoid/taxibooking.git
```

You can run unit tests I wrote myself
```
python3 motional/manage.py test taxibooking
```

To start the server, run the entrypoint.sh script. 
This builds the docker image and runs the webserver on port 8080
```
source entrypoint.sh
```

Run the tests provided by Motional
```
python3 basic_solution_checker.py
```

## More information

This app was developed in Python 3 using the Django web framework

Django was chosen for the maturity of the framework (since 2005)

Django comes provided with an ORM, a test framework, and plentiful documentation at https://docs.djangoproject.com/en/3.1/

This "batteries-included" framework allowed me to develop the taxibooking app within a single day.

There is also 100% test coverage of motional/taxibooking/views.py. See motional/taxibooking/tests.py

motional/taxibooking/models.py provides a list of models used.

This app has been dockerized (See ./Dockerfile). 

You can use ./entrypoint.sh to build and run the app