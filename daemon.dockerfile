FROM python:3

RUN mkdir -p /opt/src/store/daemon
WORKDIR /opt/src/store/daemon

COPY Store/Commons Store/Commons
COPY Store/Daemon Store/Daemon

RUN pip install -r Store/Daemon/requirements.txt

ENV PYTHONPATH="/opt/src/store/daemon"

ENTRYPOINT ["python", "./Store/Daemon/application.py"]