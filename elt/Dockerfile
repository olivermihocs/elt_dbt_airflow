FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client-15 cron

COPY start.sh /app/start.sh
COPY script.py .

WORKDIR /app

RUN echo "30 12 * * * python /app/script.py" | crontab -

CMD [ "python" , "script.py" ]