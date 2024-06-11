
FROM apache/airflow:2.7.2-python3.9

COPY requirements.txt /opt/airflow/

USER root
RUN apt-get update && apt-get install -y gcc python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
