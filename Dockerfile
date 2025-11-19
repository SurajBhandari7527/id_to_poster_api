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
# FIX: Changed to 1 worker and 4 threads to save memory (prevent OOM errors)
# Threads share memory, Workers duplicate it.
CMD ["gunicorn", "--workers", "1", "--threads", "4", "--bind", "0.0.0.0:8000", "app:app"]