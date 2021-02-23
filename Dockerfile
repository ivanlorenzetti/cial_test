FROM python:3.8

RUN mkdir app
RUN mkdir -p /app/log
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py .
COPY /cial_test ./cial_test

WORKDIR /app

RUN ls -la

# command to run on container start
CMD  python -m bot
