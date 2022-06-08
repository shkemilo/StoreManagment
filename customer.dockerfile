FROM python:3

RUN mkdir -p /opt/src/store/customer
WORKDIR /opt/src/store/customer

COPY Commons Commons
COPY Store/Commons Store/Commons
COPY Store/Customer Store/Customer

RUN pip install -r Store/Customer/requirements.txt

ENV PYTHONPATH="/opt/src/store/customer"

ENTRYPOINT ["python", "./Store/Customer/application.py"]