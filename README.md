# Taxicab booking service

## Taxi booking system

### Problem statement

You are tasked to implement a simple taxi booking system in a 2D grid world with the following criteria:

- The 2D grid world consists of `x` and `y` axis that each fit in a 32 bit integer, i.e. `-2,147,483,648` to `2,147,483,647`.
- There are **3** cars in the system, All three cars should have id `1`, `2` and `3` respectively and initial start location is at origin `(0, 0)`. Note that you can store the car states in memory and there is no need for persistent storage for this exercise.
- A car travels through the grid system will require **1 time unit** to move along the `x` or `y` axis by **1 unit** (i.e. Manhattan distance). For example
  - Car at `(0, 0)` will reach `(0, 2)` in 2 time units.
  - Car at `(1, 1)` will reach `(4, 4)` in 6 time units.
  - More than 1 car can be at the same point at any time.

### APIs

Your service should be running on PORT 8080. For simplicity, you

- **DO NOT** need to implement any form persistent storage. **In memory** data structures will be sufficient for this exercise.
- **DO NOT** need to handle concurrent API calls/data races. The APIs will be triggered **serially**.

There are 3 REST APIs you will need to implement.

#### `POST /api/book`

Your system should pick the nearest available car to the customer location and return the total time taken to travel from the current car location to customer location then to customer destination.

- Request payload

```json
{
  "source": {
    "x": x1,
    "y": y1
  },
  "destination": {
    "x": x2,
    "y": y2
  }
}
```

- Response payload

```json
{
  "car_id": id,
  "total_time": t
}
```

- All car are available initially, and become booked once it is assigned to a customer. It will remain booked until it reaches its destination, and immediately become available again.
- In the event that there are more than one car near the customer location, your service should return the car with the smallest id.
- Only one car be assigned to a customer, and only one customer to a car.
- Cars can occupy the same spot, e.g. car 1 and 2 can be at point (1, 1) at the same time.
- If there is no available car that can satisfy the request, your service should return an empty response, not an error

#### `POST /api/tick`

To facilitate the review of this exercise, your service should expose `/api/tick` REST endpoint, when called should advance your service time stamp by 1 time unit.

#### `PUT /api/reset`

Your service should also provide `/api/reset` REST endpoint, when called will reset all cars data back to the initial state regardless of cars that are currently booked.

Run the test cases in the file [basic_solution_checker.py](basic_solution_checker.py) to check whether your API works correctly

```python
python3 basic_solution_checker.py
```

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