# Use a base image for Airflow. This image already has Python installed.
FROM apache/airflow:2.7.0

# Set the AIRFLOW_HOME environment variable
ENV AIRFLOW_HOME=/opt/airflow

# Install system dependencies.
USER root
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container.
USER airflow
COPY requirements.txt .

# Install Python dependencies from the requirements.txt file.
RUN pip install --no-cache-dir -r requirements.txt
