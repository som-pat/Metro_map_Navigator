FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP=base.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

# docker build -t flask-app:v1.0 .
# docker run -d -p 5000:5000 flask-app:v1.0 
# docker container ls
# docker conatiner stop __(container  1st 4 atleast)
