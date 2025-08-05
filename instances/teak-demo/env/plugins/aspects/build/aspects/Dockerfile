FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN git clone -b v4.0.3 https://github.com/openedx/aspects-dbt aspects-dbt

WORKDIR /app/aspects-dbt

RUN pip install -r requirements.txt

RUN dbt deps

WORKDIR /app