# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
COPY . .
RUN pip3 install -r scrapy/requirements.txt
ENTRYPOINT ["./scripts/run-in-container.sh $PORT"]