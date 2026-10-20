FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir Flask==3.1.1
COPY app.py .
CMD ["python", "-u", "app.py"]
