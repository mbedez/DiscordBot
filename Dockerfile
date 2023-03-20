FROM python:3.8

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

RUN apt update
RUN apt install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl --force-reinstall

COPY . .

CMD ["python3.8", "main.py"]