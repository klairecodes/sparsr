#FROM python:3.10.9-bullseye
FROM debian:bookworm

RUN ["apt", "update"]
RUN ["apt", "install", "-y", "python3", "python3-pip"]
RUN ["apt", "install", "-y", "ffmpeg", "libsm6", "libxext6"]

WORKDIR /app
COPY . /app
RUN ["pip", "install", "--root-user-action=ignore", "-r", "requirements.txt"]

ENTRYPOINT ["python3"]
CMD ["potter-parse.py"]
