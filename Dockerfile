FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/store/


COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/store

EXPOSE 8000

ENTRYPOINT ["/bin/bash", ""]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
