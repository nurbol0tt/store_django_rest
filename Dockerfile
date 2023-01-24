FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#FROM python:3.10
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#
#WORKDIR /usr/src/store
#
#COPY ./requirements.txt /usr/src/requirements.txt
#RUN pip install -r /usr/src/requirements.txt
#
#COPY . /usr/src/store
#
#
#EXPOSE 8000