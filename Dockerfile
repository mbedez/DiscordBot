FROM arm32v7/python:3.11.2-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apk add zlib-dev \
 && apk add jpeg-dev \
 && apk add build-base \
 && apk add ffmpeg-libs \
 && apk add ffmpeg \
 && apk add git \
 && apk add libffi-dev \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl --force-reinstall \
 && apk del zlib-dev \
 && apk del jpeg-dev \
 && apk del build-base \
 && apk del git

CMD ["python3.11", "main.py"]