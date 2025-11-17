# Start with a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the file with the dependencies first to leverage Docker layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Set the command to run the application using Gunicorn
# This is a more robust server for production environments
# It runs 4 worker processes to handle requests
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]