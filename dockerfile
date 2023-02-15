FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt



RUN pip3 install -r requirements.txt

RUN apk update && apk add --no-cache cronie

COPY . . 

COPY crontab /etc/crontabs/root
RUN chmod 0644 /etc/crontabs/root
RUN /usr/sbin/crond /etc/crontabs/root

# run crond as main process of container
CMD ["/usr/sbin/crond", "-f"]