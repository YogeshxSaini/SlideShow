# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Define the command to run your application
# Use Gunicorn for production-grade server handling
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

