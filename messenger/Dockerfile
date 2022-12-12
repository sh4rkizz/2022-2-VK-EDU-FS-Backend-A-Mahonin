FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /messenger
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /messenger/