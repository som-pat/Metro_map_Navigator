# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Entrypoint script
RUN chmod +x ./entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# docker build -t flask-app:v1.0 .
# docker run -d -p 5000:5000 flask-app:v1.0 
# docker container ls
# docker conatiner stop __