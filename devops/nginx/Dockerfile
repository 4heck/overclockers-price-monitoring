FROM nginx:1.15.7-alpine

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# Set timezone
RUN apk add tzdata && cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" >  /etc/timezone

COPY nginx.conf /etc/nginx/

RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && adduser -D -H -u 1000 -s /bin/bash www-data

ARG APP_UPSTREAM_CONTAINER=app
ARG APP_UPSTREAM_PORT=5000

# Set upstream conf and remove the default conf
RUN echo "upstream app { server ${APP_UPSTREAM_CONTAINER}:${APP_UPSTREAM_PORT}; keepalive 100; }" > /etc/nginx/conf.d/upstream.conf \
    && rm /etc/nginx/conf.d/default.conf

CMD ["nginx"]

EXPOSE 80 443