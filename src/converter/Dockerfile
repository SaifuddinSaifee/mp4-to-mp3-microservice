# Use the official Python 3.11 image for bookworms as the base image
FROM python:3.11-bookworm

# Update package lists and install essential tools and libraries
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential ffmpeg \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file from the host to the container's working directory
COPY requirements.txt .

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files from the host to the container's working directory
COPY . .

# No need to expose this, as it acts on it's own

# Set the default command to run when the container starts
CMD ["python3", "consumer.py"]
