FROM python:3.10.16-slim

WORKDIR /ui

COPY ./ui /ui

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip && pip install -r fe_requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
