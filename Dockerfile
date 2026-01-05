FROM apache/airflow:2.8.1-python3.10

ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

USER root

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/airflow

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY pyproject.toml .
COPY alembic ./alembic
COPY config ./config
COPY db ./db
COPY pipeline ./pipeline
COPY scrapers ./scrapers
COPY utils ./utils
COPY alembic.ini .

RUN pip install -e .

COPY dags ./dags

ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags

CMD ["airflow", "version"]

