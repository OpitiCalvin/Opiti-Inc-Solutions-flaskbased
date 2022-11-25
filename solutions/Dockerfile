FROM python:3.7.13-alpine3.16

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install -U pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD ["main.py", "runserver"]