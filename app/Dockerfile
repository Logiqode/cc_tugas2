FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install mysql-connector-python

COPY . .

CMD ["python", "server.py"]