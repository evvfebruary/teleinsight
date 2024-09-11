# Use an official Python runtime as a parent image
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/usr/src/app
CMD ["python", "ingestor/new_messages_handler.py"]
