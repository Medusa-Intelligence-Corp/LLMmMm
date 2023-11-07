# Use the official Debian slim image as a parent image
FROM debian:bullseye-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables to:
# - Prevent Python from writing pyc files to disc (optional)
# - Prevent Python from buffering stdout and stderr (optional)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir flask openai gunicorn

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run the application using Gunicorn
# to run this locally you want to change the port to 5000
# to deploy on a server, probably change to port 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
