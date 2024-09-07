from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator #for the elt script
from airflow.operators.bash import BashOperator #for interaction with bash
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess



#Run elt script
def run_script():
    script_path = "/opt/airflow/elt/script.py" #direct path inside the docker container
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed : {result.stderr}")
    else:
        print(result.stdout)

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email_on_failure' : False,
    'email_on_retry' : False
}

dag = DAG(
    'elt_dbt_dag',
    default_args = default_args,
    description = 'ELT workflow with dbt',
    start_date = datetime(2024,9,7),
    catchup=False
)

#ELT Script
task1 = PythonOperator(
    task_id = "run_script",
    python_callable = run_script,
    dag = dag
)

#DBT (similar to data from docker-compose)
task2 = DockerOperator(
    task_id = "dbt_run",
    image ='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command = [
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt"
    ],
    auto_remove = True, #Auto remove this container if it is finished
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts = [ #mount the same volumes so airflow sees 
        Mount(source='C:/Users/Olee/.dbt', target='/root', type = 'bind'), #local path to /.dbt folder [Replace on local machine]
        Mount(source='C:/Users/Olee/projects/elt_dbt/dbt_project', target='/opt/dbt', type = 'bind') #local path to the dbt_project [Replace on local machine]
    ],
    dag = dag
)

#Order, priority
task1 >> task2 