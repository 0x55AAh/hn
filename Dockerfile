FROM python:3
MAINTAINER Lysenko Vladimir

ENV PYTHONUNBUFFERED 1

RUN mkdir /hn
WORKDIR /hn
COPY requirements.txt /hn/
RUN pip install -r requirements.txt
COPY . /hn/