FROM python:3.9-slim as base

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src /home/src

COPY tests /home/tests

EXPOSE 5000

WORKDIR /home

CMD [ "python", "src/app.py" ]
