FROM python:3.8.3-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY motional .

EXPOSE 8080

RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]