FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY reconcile.py .

RUN mkdir -p data output

CMD ["python3", "reconcile.py"]
