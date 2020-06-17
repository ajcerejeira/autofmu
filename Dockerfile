FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc-x86-64-linux-gnu \
    gcc-i686-linux-gnu \
    gcc-mingw-w64 \
    gcc-mingw-w64-i686

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml poetry.lock README.rst LICENSE src/ tests/ .

RUN pip install .

ENTRYPOINT ["autofmu"]