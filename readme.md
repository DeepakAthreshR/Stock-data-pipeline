Stock Data Ingestion Pipeline with Apache Airflow and Docker
This project sets up a data pipeline using Apache Airflow to periodically fetch stock market data from an external API and store it in a PostgreSQL database. The entire setup is containerized using Docker and Docker Compose for easy deployment and management.

Project Structure
docker-compose.yml: Defines the services for the pipeline, including PostgreSQL, Airflow's webserver, scheduler, and an initialization service.

Dockerfile: Used to build the custom Docker image for Airflow, installing necessary Python and system dependencies.

requirements.txt: Lists the Python libraries required for the pipeline, such as requests and psycopg2-binary.

dags/: This directory contains the Airflow Directed Acyclic Graphs (DAGs).

stock_data_dag.py: The Airflow DAG that orchestrates the data fetching and storage process.

stock_api_script.py: A Python script that connects to a stock API, fetches data, and inserts it into the PostgreSQL database.

.env: A file to store your sensitive environment variables (not to be committed to version control).

Prerequisites
Docker and Docker Compose installed on your system.

Setup and Configuration
Create a .env file:
In the root directory of your project, create a file named .env. This file will store your API key and a secret key for Airflow.

STOCK_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
AIRFLOW_SECRET_KEY=YOUR_SECURE_RANDOM_KEY

YOUR_ALPHA_VANTAGE_API_KEY: Replace this with your actual API key from Alpha Vantage.

YOUR_SECURE_RANDOM_KEY: Generate a secure secret key using the following Python command in your terminal: python -c "import secrets; print(secrets.token_hex(16))".

Build and Run the Containers:
Open your terminal, navigate to the project directory, and run the following command to build the Docker images and start all the services in detached mode:

docker-compose up --build -d

This command will:

Build the airflow image using your Dockerfile.

Start the postgres database service.

Run the airflow-init service to initialize the database and create an admin user.

Start the airflow-webserver and airflow-scheduler services.

Using the Airflow UI
Once the containers are running, you can access the Airflow web interface at:

http://localhost:8082

Username: airflow

Password: airflow

In the Airflow UI, you should see a DAG named stock_data_pipeline_v2. You can manually trigger this DAG or wait for its scheduled run to start the data ingestion process.

Troubleshooting
403 Forbidden Error: If you see a 403 Forbidden error, ensure that the AIRFLOW_SECRET_KEY in your .env file is the same across all Airflow services in the docker-compose.yml file.

API Connectivity Issues: If the DAG fails, check the logs of the fetch_and_store_data task. The error Could not read served logs: [Errno -2] Name or service not known likely indicates an issue with the API endpoint URL in the stock_api_script.py file. Ensure you have the correct and functional API endpoint.

Contact
Email : deepakr0320@gmail.com