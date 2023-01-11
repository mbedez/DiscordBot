FROM python:3.8

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

RUN apt update
RUN apt install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3.8", "main.py"]