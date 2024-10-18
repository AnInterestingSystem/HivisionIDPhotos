FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY hivision ./hivision
COPY app.py .
COPY ui ./ui

EXPOSE 8080

ENV ENV=prod

CMD ["python", "app.py", "--port", "8080"]