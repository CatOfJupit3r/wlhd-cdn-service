FROM python:3.12.0

WORKDIR /app

COPY . .

RUN pip install -e .

CMD ["python", "main.py"]
