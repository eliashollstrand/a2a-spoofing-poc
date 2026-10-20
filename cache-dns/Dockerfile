FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir dnslib==0.9.26
COPY dns_server.py .
CMD ["python", "-u", "dns_server.py"]
