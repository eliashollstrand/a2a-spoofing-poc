FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests==2.32.3 requests-cache==1.2.1
COPY client.py .
CMD ["python", "-u", "client.py"]
