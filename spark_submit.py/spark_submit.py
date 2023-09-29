 spark_submit = BashOperator(
        task_id='spark_submit',
        bash_command="spark-submit /var/lib/postgresql/dags/spark_submit.py",
    )
