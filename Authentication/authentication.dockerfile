FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY src/requirements.txt requirements.txt

COPY src/commons commons/
COPY src/authentication .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]