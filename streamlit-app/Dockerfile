FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl

COPY . /app/

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD ["CMD", "curl", "--fail", "http://localhost:8501/_stcore/health"]

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--global.logLevel=debug"]