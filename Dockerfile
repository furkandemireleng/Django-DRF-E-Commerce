#dowload python image
FROM python:3.10-slim-buster

# Base image

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install project dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /usr/src/app/

# Copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Run the entrypoint.sh script as the entrypoint of the container
ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]
# Collect static files
# Run the command to start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]