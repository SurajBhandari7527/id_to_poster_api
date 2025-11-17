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
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]```

### How to Build and Run the Docker Container

Make sure you have [Docker installed](https://docs.docker.com/get-docker/) on your machine.

1.  **Navigate to your project directory:**
    Open your terminal or command prompt and change to the directory where you saved the four files (`/flask-poster-api`).

2.  **Build the Docker image:**
    Run the following command. This will read the `Dockerfile`, download the base image, install your dependencies, and create a container image named `poster-api`. The `.` at the end is important as it specifies the current directory as the build context.

    ```bash
    docker build -t poster-api .
    ```

3.  **Run the Docker container:**
    Once the image is built successfully, run it with the following command. This starts a container from your `poster-api` image.

    *   `-d`: Runs the container in detached mode (in the background).
    *   `-p 8080:8000`: Maps port 8080 on your local machine to port 8000 inside the container (which is where Gunicorn is running). You can change `8080` to any other available port on your machine.
    *   `--name my-poster-app`: Gives a convenient name to your running container.

    ```bash
    docker run -d -p 8080:8000 --name my-poster-app poster-api
    ```

4.  **Test the API:**
    Your API is now running and accessible on your local machine. You can test it just like before, but using the new port (`8080` in this example).

    Open your browser and go to:
    `http://localhost:8080/get_poster?imdb_id=tt0468569`

    Or use `curl` in your terminal:

    ```bash
    curl "http://localhost:8080/get_poster?imdb_id=tt0468569"
    ```

    You should receive the same JSON response as before.

### Docker Commands Cheatsheet

*   **List running containers:** `docker ps`
*   **Stop the container:** `docker stop my-poster-app`
*   **Start the container again:** `docker start my-poster-app`
*   **View container logs:** `docker logs my-poster-app`
*   **Remove the container (must be stopped first):** `docker rm my-poster-app`
*   **List all local Docker images:** `docker images`
*   **Remove the Docker image:** `docker rmi poster-api`