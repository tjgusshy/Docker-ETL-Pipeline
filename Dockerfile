# Base Image: A lightweight Linux with Python pre-installed
FROM python:3.9-slim

# Set the folder where we work inside the container
WORKDIR /app

# Install Cron (Linux tool) because Python slim images don't have it
RUN apt-get update && apt-get install -y cron

# Copy requirements first to leverage Docker Cache (speeds up re-builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY main.py .
COPY crontab /etc/cron.d/etl-cron

# Give Cron permission to run the file
RUN chmod 0644 /etc/cron.d/etl-cron

# Register the cron job
RUN crontab /etc/cron.d/etl-cron

# Create the log file so we can watch it
RUN touch /var/log/cron.log

# CMD: Start Cron AND watch the log file (keeps container running)

CMD cron && tail -f /var/log/cron.log