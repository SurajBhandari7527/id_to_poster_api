# Start with a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (app.py and Poster_df_final.csv)
COPY . .

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Set the command to run the application using Gunicorn
# We bind to port 8000 as specified in EXPOSE
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]