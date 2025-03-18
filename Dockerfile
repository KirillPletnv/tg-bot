
FROM python:3.9-slim


WORKDIR /app

COPY requirements1.txt .

RUN pip install --no-cache-dir -r requirements1.txt

COPY . .

CMD ["python", "tg_bot.py"]