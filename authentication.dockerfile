FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY Commons/ Commons/
COPY Authentication/ Authentication/

RUN pip install -r Authentication/requirements.txt

ENV PYTHONPATH="/opt/src/authentication"

ENTRYPOINT ["python", "./Authentication/application.py"]