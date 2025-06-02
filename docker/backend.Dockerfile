FROM python:3.10.16-slim

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt /app

RUN apt-get update && apt-get install -y curl

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
