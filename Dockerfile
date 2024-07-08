# Use the official Python image from the Docker Hub
FROM python:3.10


# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "transit:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

