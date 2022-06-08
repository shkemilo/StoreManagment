FROM python:3

RUN mkdir -p /opt/src/store/admin
WORKDIR /opt/src/store/admin

COPY Commons Commons
COPY Store/Commons Store/Commons
COPY Store/Admin Store/Admin

RUN pip install -r Store/Admin/requirements.txt

ENV PYTHONPATH="/opt/src/store/admin"

ENTRYPOINT ["python", "./Store/Admin/application.py"]