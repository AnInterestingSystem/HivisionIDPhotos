FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev

COPY hivision ./hivision
COPY app.py .
COPY ui ./ui

RUN uv sync --locked --no-dev

EXPOSE 8080

ENV PYTHONIOENCODING=utf-8
ENV ENV=prod
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "app.py", "--port", "8080"]