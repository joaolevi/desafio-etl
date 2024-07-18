FROM alpine:latest

RUN apk update
RUN apk add --no-cache curl jq tzdata
RUN apk add bash
RUN rm -rf /var/cache/apk/*
RUN apk add --no-cache dos2unix

# Adicione o arquivo cron
COPY ../docker/crontab/files/file /etc/cron.d/file

# Dê permissão de execução
RUN chmod 777 /etc/cron.d/file

# Crie o log (opcional)
RUN touch /var/log/cron.log

RUN chmod 777 /var/log/cron.log

RUN mkdir /scriptcron
# Copie o script de entrada para o contêiner e torne-o executável
COPY ../docker/crontab/scripts/entrypoint.sh /scriptcron/entrypoint.sh

RUN chmod +x /scriptcron/entrypoint.sh

# Defina o script como ponto de entrada
ENTRYPOINT ["/scriptcron/entrypoint.sh"]