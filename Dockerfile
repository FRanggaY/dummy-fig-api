# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# copy
COPY . .

# Copy the requirements file and install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run your FastAPI app (for live server)
CMD uvicorn --host 0.0.0.0 --port 8120 app.main:app
