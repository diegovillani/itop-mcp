FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY manifest.json .

EXPOSE 9000

CMD ["python", "src/server.py"]

