# app/Dockerfile

#FROM python:3.8-slim
FROM aminehy/docker-streamlit-app:latest

WORKDIR /app

RUN git clone https://github.com/robinsonkwame/csdt-structural-style-transfer .

RUN pip3 install -r requirements_9_11_2023.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=192.168.0.101"]