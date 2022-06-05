FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY src/ .

RUN pip install -r requirements.txt

ENV PYTHONPATH="/opt/src/authentication"

ENTRYPOINT ["python", "./application.py"]