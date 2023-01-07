#FROM python:3.10.9-bullseye
FROM debian:bookworm

WORKDIR /app

RUN ["apt", "update"]
RUN ["apt", "install", "-y", "python3", "python3-pip"]
RUN ["apt", "install", "-y", "ffmpeg", "libsm6", "libxext6"]

COPY requirements.txt /app
RUN ["pip", "install", "--root-user-action=ignore", "-r", "requirements.txt"]

COPY . /app

ENTRYPOINT ["python3", "subtitle_parse.py"]
