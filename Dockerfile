FROM ubuntu:latest
LABEL authors="albz"

ENTRYPOINT ["top", "-b"]