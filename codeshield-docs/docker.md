# Docker Deployment Guide

Run CodeShield AI in containerized environments for consistent, reproducible security scanning.

## Quick Start

### Pull and Run (Once Available)

```bash
# Pull the image
docker pull lydiamorgan/codeshield-ai:latest

# Scan your code
docker run -v $(pwd):/code lydiamorgan/codeshield-ai:latest /code
```

## Build Your Own Image

### Dockerfile

Create `Dockerfile` in your project:

```dockerfile
FROM node:18-alpine

# Install dependencies
RUN apk add --no-cache git

# Set working directory
WORKDIR /app

# Clone CodeShield AI
RUN git clone https://github.com/Lydiamorgan85/codeshield-ai.git . && \
    npm ci --only=production

# Create volume mount point
VOLUME /code

# Set entrypoint
ENTRYPOINT ["npx", "codeshield"]

# Default command
CMD ["analyze", "/code"]
```

### Build the Image

```bash
docker build -t codeshield:latest .
```

## Usage Examples

### Scan Local Directory

```bash
docker run -v $(pwd):/code codeshield:latest analyze /code
```

### Output to File

```bash
docker run -v $(pwd):/code -v $(pwd)/reports:/reports \
  codeshield:latest analyze /code --output /reports/scan.json
```

### Custom Configuration

```bash
docker run -v $(pwd):/code -v $(pwd)/.codeshield.json:/app/.codeshield.json \
  codeshield:latest analyze /code
```

### Fail on Critical Issues

```bash
docker run -v $(pwd):/code \
  codeshield:latest analyze /code --fail-on-critical
```

## Docker Compose

### Basic Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  codeshield:
    build: .
    volumes:
      - ./src:/code
      - ./reports:/reports
    command: analyze /code --output /reports/scan.json
```

Run:

```bash
docker-compose up
```

### Multi-Service Pipeline

```yaml
version: '3.8'

services:
  codeshield-scan:
    image: codeshield:latest
    volumes:
      - ./src:/code
      - ./reports:/reports
    command: analyze /code --output /reports/scan.json
    
  report-server:
    image: nginx:alpine
    volumes:
      - ./reports:/usr/share/nginx/html
    ports:
      - "8080:80"
    depends_on:
      - codeshield-scan
```

## Kubernetes Deployment

### Job for Security Scanning

Create `codeshield-job.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: codeshield-security-scan
spec:
  template:
    spec:
      containers:
      - name: codeshield
        image: codeshield:latest
        command: ["npx", "codeshield", "analyze", "/code"]
        volumeMounts:
        - name: source-code
          mountPath: /code
        - name: reports
          mountPath: /reports
      volumes:
      - name: source-code
        persistentVolumeClaim:
          claimName: code-pvc
      - name: reports
        persistentVolumeClaim:
          claimName: reports-pvc
      restartPolicy: Never
  backoffLimit: 3
```

Apply:

```bash
kubectl apply -f codeshield-job.yaml
```

### CronJob for Scheduled Scans

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: codeshield-daily-scan
spec:
  schedule: "0 2 * * *"  # Run at 2 AM daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: codeshield
            image: codeshield:latest
            command: ["npx", "codeshield", "analyze", "/code", "--output", "/reports/daily-scan.json"]
            volumeMounts:
            - name: source-code
              mountPath: /code
            - name: reports
              mountPath: /reports
          volumes:
          - name: source-code
            persistentVolumeClaim:
              claimName: code-pvc
          - name: reports
            persistentVolumeClaim:
              claimName: reports-pvc
          restartPolicy: OnFailure
```

## Environment Variables

Configure via environment variables:

```bash
docker run -e CODESHIELD_SEVERITY=critical,high \
           -e CODESHIELD_OUTPUT_FORMAT=json \
           -v $(pwd):/code \
           codeshield:latest analyze /code
```

Available variables:

```dockerfile
ENV CODESHIELD_SEVERITY="critical,high,medium"
ENV CODESHIELD_OUTPUT_FORMAT="json"
ENV CODESHIELD_FAIL_ON_CRITICAL="true"
ENV CODESHIELD_LOG_LEVEL="info"
```

## Optimized Production Image

### Multi-stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /build
RUN git clone https://github.com/Lydiamorgan85/codeshield-ai.git .
RUN npm ci --only=production

# Production stage
FROM node:18-alpine

# Add non-root user
RUN addgroup -g 1001 codeshield && \
    adduser -D -u 1001 -G codeshield codeshield

WORKDIR /app

# Copy from builder
COPY --from=builder --chown=codeshield:codeshield /build /app

# Switch to non-root user
USER codeshield

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node --version || exit 1

VOLUME /code
ENTRYPOINT ["npx", "codeshield"]
CMD ["analyze", "/code"]
```

## CI/CD Integration

### GitHub Actions with Docker

```yaml
name: Docker Security Scan

on: [push]

jobs:
  scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build CodeShield Image
      run: docker build -t codeshield:latest .
    
    - name: Run Security Scan
      run: |
        docker run -v $(pwd):/code \
                   -v $(pwd)/reports:/reports \
                   codeshield:latest analyze /code --output /reports/scan.json
    
    - name: Upload Report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: reports/scan.json
```

### GitLab CI with Docker

```yaml
security_scan:
  image: docker:latest
  services:
    - docker:dind
  
  script:
    - docker build -t codeshield:latest .
    - docker run -v $(pwd):/code codeshield:latest analyze /code
```

## Docker Hub Publishing

### Tag and Push

```bash
# Tag image
docker tag codeshield:latest lydiamorgan/codeshield-ai:latest
docker tag codeshield:latest lydiamorgan/codeshield-ai:v1.0.0

# Push to Docker Hub
docker push lydiamorgan/codeshield-ai:latest
docker push lydiamorgan/codeshield-ai:v1.0.0
```

### Automated Build

Create `.github/workflows/docker-publish.yml`:

```yaml
name: Publish Docker Image

on:
  release:
    types: [published]

jobs:
  push_to_registry:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          lydiamorgan/codeshield-ai:latest
          lydiamorgan/codeshield-ai:${{ github.event.release.tag_name }}
```

## Performance Optimization

### Layer Caching

```dockerfile
# Cache dependencies separately
FROM node:18-alpine

WORKDIR /app

# Copy package files first
COPY package*.json ./
RUN npm ci --only=production

# Then copy source code
COPY . .
```

### Smaller Image Size

```dockerfile
# Use Alpine for smaller size
FROM node:18-alpine

# Clean up after install
RUN npm ci --only=production && \
    npm cache clean --force && \
    rm -rf /tmp/*
```

## Troubleshooting

### Permission Issues

```bash
# Run with correct permissions
docker run --user $(id -u):$(id -g) \
           -v $(pwd):/code \
           codeshield:latest
```

### Volume Mount Problems

```bash
# Use absolute paths
docker run -v /absolute/path/to/code:/code codeshield:latest
```

### Out of Memory

```bash
# Increase memory limit
docker run --memory=2g -v $(pwd):/code codeshield:latest
```

## Security Best Practices

1. **Run as non-root user** - Avoid privilege escalation
2. **Use official base images** - Ensure supply chain security
3. **Scan the scanner** - Security scan your Docker images
4. **Keep images updated** - Regularly rebuild with latest base
5. **Limit container capabilities** - Use `--cap-drop=ALL`

## Examples

### Scan on Every Commit

```bash
#!/bin/bash
# pre-commit hook

docker run -v $(pwd):/code codeshield:latest analyze /code --fail-on-critical
if [ $? -ne 0 ]; then
    echo "Security issues detected. Commit blocked."
    exit 1
fi
```

### Scheduled Security Reports

```bash
#!/bin/bash
# cron job: 0 2 * * * /path/to/scan.sh

docker run -v /var/www/app:/code \
           -v /var/reports:/reports \
           codeshield:latest analyze /code \
           --output /reports/daily-$(date +%Y%m%d).json
```

## Support

Issues with Docker deployment?
- Check [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Email: lydiamorgan000@gmail.com
