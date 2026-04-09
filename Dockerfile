FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PORT=8000

COPY --chmod=+x entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]