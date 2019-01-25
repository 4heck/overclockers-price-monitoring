FROM python:3.6-alpine

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# Set timezone
RUN apk add tzdata && cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" >  /etc/timezone

# create app path
RUN mkdir -p /app
WORKDIR /app

# Add a non-root user to prevent files being created with root permissions on host machine.
ARG USER=app
ARG UID=1000
ARG HOME=/app
RUN adduser -u $UID -s /bin/bash -D -h $HOME $USER

# install persistent dependencies
RUN apk add --update --no-cache postgresql-dev gcc musl-dev make libxslt-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# install temporary dependencies
RUN apk add --update --no-cache --virtual .build-deps \
	shadow python3-dev libc-dev libc6-compat zlib-dev libffi-dev ca-certificates

# update pip
RUN pip install pip==18.0

# install pipenv
RUN pip3 install pipenv==2018.7.1

# install apk
RUN apk add --update --no-cache postgresql-dev gcc musl-dev make libxslt-dev

### supervisor
EXPOSE 9001
RUN apk update && apk add git
RUN pip install git+https://github.com/Supervisor/supervisor # supervisor with support python 3
ADD ./devops/app/supervisor /etc/supervisor
RUN mkdir /var/log/supervisor

# copy application code
ADD . /app
RUN chown -R app:app /app

# install packages
RUN pipenv install --deploy --system # --skip-lock

# apk del
RUN apk del .build-deps && \
	rm -rf /var/cache/apk/* /root/.cache /tmp/*

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisor/supervisord.conf"]
