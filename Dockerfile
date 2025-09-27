FROM python:3.13-slim AS builder
WORKDIR /app
    

RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    

FROM python:3.13-slim
WORKDIR /app
    
COPY --from=builder /install /usr/local
    
ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages
    
COPY . .
    
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
