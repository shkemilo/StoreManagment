FROM python:3

RUN mkdir -p /opt/src/store/warehouse
WORKDIR /opt/src/store/warehouse

COPY Commons Commons
COPY Store/Warehouse Store/Warehouse

RUN pip install -r Store/Warehouse/requirements.txt

ENV PYTHONPATH="/opt/src/store/warehouse"

ENTRYPOINT ["python", "./Store/Warehouse/application.py"]