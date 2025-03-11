FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV BOT_TOKEN=8068745600:AAGoX4QS36XHK-V7PiF6pX3idkj5pWDN1NQ
ENV CHANNEL_ID=-1002212704190

CMD ["python", "bot.py"]