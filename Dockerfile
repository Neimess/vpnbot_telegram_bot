FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

COPY . /app

RUN ["uv", "sync", "--no-dev"]

CMD ["uv", "run", "--no-cache", "__main__.py" ]