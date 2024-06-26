# Use the official Python 3.11 image for bookworms as the base image
FROM python:3.11-bookworm

# Update package lists and install essential tools and libraries
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file from the host to the container's working directory
COPY ./requirements.txt /app

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the project files from the host to the container's working directory
COPY . /app

# Expose port 5000 to allow external connections to the container
EXPOSE 5000

# Set the default command to run when the container starts
CMD ["python3", "server.py"]
