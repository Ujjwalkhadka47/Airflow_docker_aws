Apache Airflow with Docker & Postgres

Author:
Ujjwal Khadka - ujjwalkhadka@fusemachines.com

This project guide will help you set up an Apache Airflow environment within a Docker container, based on your existing Apache Airflow  and dump the data in postgres and read it back.

# Prerequisites

To install Apache Airflow in your MacOS follw this guide : https://arpitrana.medium.com/install-airflow-on-macos-guide-fc66399b2a9e

Before proceeding, ensure Docker is installed in your system following this guide :
https://docs.docker.com/desktop/install/mac-install/

Now, we will Dockerize our Apache Airflow and finally dump and read data from postgres, encapsulating it within a Docker container.

Create a Dockerfile: In the root directory of your project, create a file named docker-compose.yaml. This file will contain instructions on how to build the Docker image for your project. 


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV AIRFLOW_HOME=/app/airflow

# Initialize Airflow database and create docker-compose
RUN airflow db init
docker-compose.yaml

# Create a user for Airflow (Change credentials as needed) in .yaml file
RUN airflow users create \
    --username admin \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email admin@example.com \
    --password admin

# Create a postgres connection in .yaml file
 postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    ports:
      - 5433:5432

# Start the Airflow web server and scheduler
docker compose up

Build the Docker Image: Build the Docker image by running the following command in your project's root directory (where the Dockerfile is located):

docker build -t your-airflow-image:latest .

This command tells Docker to build an image named your-airflow-image using the current directory (.) as the build context.
Run Your Apache Airflow Container: After successfully building the image, you can run your Apache Airflow container using the following command:

docker run -d -p 8080:8080 --name your-airflow-container your-airflow-image:latest
-d: Runs the container in detached mode.
-p 8080:8080: Maps port 8080 from the host to the container, which is the Airflow web UI port.
--name your-airflow-container: Assigns a name to the Docker container.
Access the Airflow Web UI: You can now access the Apache Airflow web UI by opening a web browser and navigating to http://localhost:8080.

# For HTTP Connection in Airflow
Set http connection id.
Connection Type: HTTP
Host: Your API URL
Screenshots/http_connections.png

# For Postgres Connection in Airflow
Set postgres connection id.
Connection Type: Postgres
Host: postgres
Schema: Your database name
Username: Your Postgres username
Port: 5432
Screenshots/postgres_connections.png

# For Postgres Connection in Dbeaver
port: 5433

Airflow DAG: My_DAG

# DAG Execution

This Airflow DAG, named My_DAG, is designed to perform the following tasks:

1.Check API Availability: It starts by checking the availability of an API endpoint.
2.Fetch Data from API: If the API is available, it proceeds to fetch data from the API endpoint and saves it as a JSON file.
3.Convert JSON to CSV: After fetching the data, it converts the JSON data into a CSV file and saves it.
4.Load Data into Postgres: Finally, it loads the CSV data into a PostgreSQL database table.
5.Read Data from Postgres: It reads data from the PostgreSQL database table named airflow.
6.Process Data from Postgres: After reading data from Postgres, it processes the result data and prints it.

# DAG Schedule

1.The DAG is scheduled to run daily.
2.It started running on September 19, 2023.
3.It does not perform catch-up runs for past intervals.

Your DAG code, which is located in the dags folder, will automatically be detected and loaded by Apache Airflow running within the Docker container.

# Dag Flow
Screenshots/dag_flow.png

# Final log
Screenshots/final_log.png

Conclusion

We've successfully Dockerized our Apache Airflow project, making it portable and easy to manage. We can now manage our workflows, connections, and DAGs through the Apache Airflow web UI while running it within a Docker container.