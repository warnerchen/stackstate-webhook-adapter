# Stackstate Webhook Adapter

This component acts as an intermediary proxy that receives webhook data from SUSE O11y (Stackstate), transforms it into the required format, and forwards it to the target endpoint. It also returns the HTTP status code from the endpoint back to SUSE O11y.

Currently supported data format transformations:

- WeCom

## Quick Start

### WeCom

Build the Docker image:

```bash
docker build -t <registry>/<repository>/stackstate-wecom-webhook-adapter:<tag> -f wecom_adapter/Dockerfile .
```

Replace the `image` and `WECOM_WEBHOOK_TARGET_URL` in `wecom_adapter/deploy/deployment.yaml`.

Replace the `host` in `wecom_adapter/deploy/ingress.yaml`.

Deploy to Kubernetes:

```bash
kubectl apply -f wecom_adapter/deploy/
```
