FROM python:3.6-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -U setuptools pip

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/main.py

EXPOSE 5000

CMD ["python", "app/main.py", "serve"]