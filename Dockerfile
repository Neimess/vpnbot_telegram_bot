FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt update && apt install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN ["uv", "sync", "--no-dev"]

CMD ["uv", "run", "--no-cache", "__main__.py" ]