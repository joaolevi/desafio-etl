FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app/ /app

ADD crontab /etc/cron.d/cronjob

RUN chmod 0644 /etc/cron.d/cronjob
RUN touch /var/log/cron.log
RUN apt-get update
RUN apt-get -y install cron
RUN mkdir /app/logs

CMD cron && tail -f /var/log/cron.log