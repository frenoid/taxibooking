# Motional Take Home Exercise - Done by Lim Xing Kang Norman

## Taxi booking system

## To Run

Clone the repo
```
git clone https://github.com/frenoid/taxibooking.git
```


```
docker build -t motional .
```

Run the container and expose port 8080
```
docker run -d -p 8080:8080 motional
```

Run the tests
```
python3 basic_solution_checker.py
```
