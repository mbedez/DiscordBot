FROM python:3.11.2-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apk add --no-cache zlib-dev \
 && apk add --no-cache jpeg-dev \
 && apk add --no-cache build-base \
 && apk add --no-cache ffmpeg-libs \
 && apk add --no-cache ffmpeg \
 && apk add --no-cache git \
 && apk add --no-cache libffi-dev \
 && apk add --no-cache tzdata \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del zlib-dev \
 && apk del jpeg-dev \
 && apk del build-base \
 && apk del git

ENV TZ=Europe/Paris

CMD ["python3.11", "main.py"]
