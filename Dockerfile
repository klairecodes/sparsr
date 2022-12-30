#FROM python:3.10.9-bullseye
FROM debian:bookworm

WORKDIR /app
COPY . /app

RUN ["apt", "update"]
RUN ["apt", "install", "-y", "python3", "python3-pip"]
RUN ["apt", "install", "-y", "ffmpeg", "libsm6", "libxext6"]
RUN ["pip", "install", "-r", "requirements.txt"]

ENTRYPOINT ["python3"]
CMD ["potter-parse.py"]
