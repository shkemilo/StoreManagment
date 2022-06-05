FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY src/requirements.txt requirements.txt

COPY src/commons commons/
COPY src/migration .

RUN pip install -r requirements.txt

ENV PYTHONPATH="/opt/src/authentication"

ENTRYPOINT ["python", "./migrate.py"]