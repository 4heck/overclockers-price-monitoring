FROM postgres:10.6-alpine

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# Set timezone
RUN apk add tzdata && cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" >  /etc/timezone

CMD ["postgres"]

EXPOSE 5432
