FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP=base.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

# docker build -t flask-app:v1.0 .