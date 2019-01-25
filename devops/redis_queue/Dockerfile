FROM redis:5.0.2-alpine3.8

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# Set timezone
RUN apk add tzdata && cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" >  /etc/timezone

CMD ["redis-server"]

EXPOSE 6379