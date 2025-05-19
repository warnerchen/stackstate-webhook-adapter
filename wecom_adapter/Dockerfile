FROM python:3.10.17-alpine

WORKDIR /wecom_adapter

COPY wecom_adapter/adapter.py .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir requests

ENTRYPOINT ["python3", "adapter.py", "8080"]
