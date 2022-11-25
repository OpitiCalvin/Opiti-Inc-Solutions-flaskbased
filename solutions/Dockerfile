FROM python:3.7.13-alpine3.16

# Install dependencies for GIS
RUN set -ex \
    && apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    autoconf \
    automake \
    gcc \
    gdal-dev \
    geos \
    make \
    musl-dev \
    postgresql-dev
# RUN ln -s /usr/lib/libgeos_c.so.1 /usr/local/lib/libgeos_c.so
# RUN ln -s /usr/lib/libgdal.so.20.1.0 /usr/local.lib/libgdal.so

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