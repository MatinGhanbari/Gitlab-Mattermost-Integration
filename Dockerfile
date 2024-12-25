FROM python:3.13.0

WORKDIR /app

COPY main.py .
COPY src /app/src
COPY requirements.txt .
COPY appsettings.json .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "./main.py"]
