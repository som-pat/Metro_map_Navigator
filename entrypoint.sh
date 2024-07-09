#!/bin/sh

# Run the data extraction and loading script
python Extract_load.py

# Start the FastAPI server
uvicorn transit:app --host 0.0.0.0 --port 8000 --reload