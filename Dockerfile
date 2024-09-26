FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9001
EXPOSE 8080

CMD ["sh", "-c", "python3 model.py & python3 -m http.server 8080"]
