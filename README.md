# NY Times Best Sellers Data Pipeline

A simple data pipeline...

Deployment of a data pipeline that extracts...

## Dataset

This project uses data from the New York Times Books API. Usage is subject to the Developer Terms of Use, and attribution to NYT is required for any publication or visualization of the data.

## Tools and Technologies

- Python
- PostgreSQL
- Airflow
- Docker

## Data Architecture

![alt text](NY-Times-Best-Sellers-Data-Pipeline.png)

## Process

### Pre-requisites

- Get started with NYT Public API -> [Steps](https://developer.nytimes.com/get-started)

- Make sure you've installed and running Docker Desktop or Docker Engine:
  - [Docker Desktop](https://docs.docker.com/desktop/)
  - [Docker Engine](https://docs.docker.com/engine/install/)

### Initialize Services

- Clone git repo
  ```
  git clone XXX
  cd amazon-books-data-pipeline
  ```

- Initialize airflow database
  ```
  docker compose up airflow-init
  ```

- Start services
  ```
  docker compose up
  ```

- In a second terminal check that the docker containers status is healthy
  ```
  docker ps
  ```

### Settings

- pgAdmin

  1. Log in to [pgAdmin](http://localhost:5050) with Username:'admin@admin.com' and Password:'root'.
  2. On the left pannel, right click on Servers --> Register --> Server
  3. On General tab, enter Name: "postgres".
  4. On Connection tab, enter Hostname: "postgres", Port: "5432", Username:'airflow', and Password:'airflow'.
  5. You should be connected to Postgresdb from pgAdmin and see the database "booksdb" created automatically.
     ![alt text](image.png)

- Airflow UI

  1. Log in to [Airflow UI](http://localhost:8080) with 'airflow' for both your Username and Password.
  2. Select Admin tab --> Connections --> Add Connection
  3. Enter Connection ID: "postgres_nytimes_connection" and Connection Type: "postgres"
  4. Enter Host: "postgres", Login:"airflow", Password:"airflow", Port: "5432", and Database: "booksdb".
  5. Select Admin tab --> Variables --> Add Variable
  6. Enter Key: "nytimes_api_key" and as Value your api key value provided by NY Times API.

### Run Pipeline

- On Airflow UI, select the DAG and click on Trigger.

- To stop Airflow
  ```
  docker compose down
  ```

## Remaining tasks

1. Finish project and dataset description including schedule
