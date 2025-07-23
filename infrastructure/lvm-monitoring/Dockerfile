FROM python:3.11-slim

# Install required packages
RUN pip install --no-cache-dir \
    kubernetes==28.1.0 \
    prometheus-client==0.19.0

# Create non-root user
RUN useradd -m -u 1000 metrics

# Copy script
COPY lvm-metrics-exporter.py /app/

# Set permissions
RUN chmod +x /app/lvm-metrics-exporter.py && \
    chown -R metrics:metrics /app

USER metrics
WORKDIR /app

ENTRYPOINT ["python3", "/app/lvm-metrics-exporter.py"]