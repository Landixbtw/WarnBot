# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libmariadb-dev \
    libssl-dev \
    libffi-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Python dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy your Python project files to the working directory
COPY . .

# Define environment variables if needed (e.g., Discord token)
# ENV DISCORD_TOKEN="YOUR_DISCORD_TOKEN"

# Set default command to run your Python script
CMD ["python3", "main.py"]
