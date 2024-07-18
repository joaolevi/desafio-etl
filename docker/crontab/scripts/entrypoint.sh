#!/bin/sh
set -e

# Verifica se foram passados argumentos
if [ $# -eq 0 ]
then
    # Verifica se o arquivo crontab existe no diretório /etc/cron.d/
    if [ -f "/etc/cron.d/file" ];then
       # Instala as tarefas cron
       cat /etc/cron.d/file | crontab - && crond -f -l 9 -L /dev/stdout
    else
       echo "No crontab file found in /etc/cron.d/" 
       exit 1
    fi
else
    # Se argumentos foram fornecidos, adicione-os ao arquivo de tarefas temporário
    for i in "$@"
    do
       echo "$i" >> /tmp/jobs.txt
    done
    echo "Running crontab service ..."
    # Instala as tarefas cron do arquivo temporário
    crontab /tmp/jobs.txt
fi