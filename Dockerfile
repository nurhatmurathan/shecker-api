# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.org --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PORT 8000

# Run gunicorn when the container launches
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
