# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'amit',
    'start_date': days_ago(0),
    'email': 'amitms2005@hotmail.com',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'my-first-dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(minutes=1),
)

# define the tasks

# define the first task

extract = BashOperator(
    task_id='extract',
    bash_command='cut -d":" -f1,3,6 /etc/passwd > $AIRFLOW_HOME/extracted-data.txt',
    dag=dag,
)

# define the second task
transform_and_load = BashOperator(
    task_id='transform',
    bash_command='tr ":" "," < $AIRFLOW_HOME/extracted-data.txt > $AIRFLOW_HOME/transformed-data.csv',
    dag=dag,
)

# task pipeline
extract >> transform_and_load
#export AIRFLOW_HOME=/home/project/airflow
#echo $AIRFLOW_HOME
#Airflow searches for Python source files within the specified DAGS_FOLDER. The location of DAGS_FOLDER can be located in the airflow.cfg file, where it has been configured as /home/project/airflow/dags.
# cp my_first_dag.py $AIRFLOW_HOME/dags

