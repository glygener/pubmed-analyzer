FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl apache2-utils tini && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip3 install -r requirements.txt

ENV STREAMLIT_LOGGER_LEVEL=info
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/logs
VOLUME ["/app/logs"]

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD ["curl", "--fail", "http://localhost:8501/_stcore/health"]

RUN groupadd -g 10001 analyzer_group
RUN useradd -r -u 10001 -g appgroup analyzer_user
RUN chown -R analyzer_user:analyzer_group /app
USER analyzer_user

ENTRYPOINT ["tini", "-g", "--"]
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --logger.level=${STREAMLIT_LOGGER_LEVEL} 2>&1 | rotatelogs -e -n 5 /app/logs/app.log 10M"]