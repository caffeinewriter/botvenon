FROM python:3

RUN mkdir /data

WORKDIR "/usr/src/app"
ENV IS_DOCKER 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]

VOLUME /data