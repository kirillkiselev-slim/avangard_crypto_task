FROM python:3.12-alpine
WORKDIR /bot
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH="/bot"

VOLUME /bot/data

CMD ["python3", "main.py"]
