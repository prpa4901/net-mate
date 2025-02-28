# Stage 1: Build stage
FROM python:3.12-slim AS builder
WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.12-slim
WORKDIR /backend
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8087
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8087"]