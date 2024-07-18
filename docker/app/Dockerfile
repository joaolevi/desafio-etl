FROM python:3.9

WORKDIR /app

COPY ../docker/app/requirements.txt /app
RUN pip install -r requirements.txt

COPY ../../app/ /app

CMD ["python", "app.py"]