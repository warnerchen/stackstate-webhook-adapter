FROM python:3.10.17-alpine

WORKDIR /wecom_adapter

COPY wecom_adapter/adapter.py .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir requests

ENV TINI_VERSION=v0.19.0

RUN wget -O /tini https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini && \
    chmod +x /tini

ENTRYPOINT ["/tini", "--", "python3", "adapter.py", "8080"]
