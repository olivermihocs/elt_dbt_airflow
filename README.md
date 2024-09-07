## ELT Project using Docker, dbt, PostgreSQL and Airflow

The base version of this project can be viewed here: [elt_dbt](https://github.com/olivermihocs/elt_dbt)

A new CRON job is implemented, which we can use to schedule tasks.

Airflow is used to set up a webserver and a scheduler.
The DAG for this project can be found in **airflow/dags/dag.py**

To run this project first we have to start this service and initialize airflow:

`docker compose up init-airflow -d`

Once airflow is initialized we can start the services:

`docker compose up`

After this is completed the webserver can be viewed at `localhost:8080`
(To run the *DAG* on your local machine, change the mount sources in the `task2 DockerOperator` in *dag.py*)
