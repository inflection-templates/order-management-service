# Setup using Docker

This guide shows how to set up and run the Order Management Service using Docker and Docker Compose.

## Prerequisites

- Docker 20.0+
- Docker Compose 2.0+
- Git

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd order-management-service
cp .env.example .env
```

### 2. Configure Environment

Edit the `.env` file for Docker setup:

```env
# Database (Docker setup)
DB_HOST=db
DB_PORT=3306
DB_NAME=order_management
DB_USER_NAME=order_user
DB_USER_PASSWORD=secure_password

# Application
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
BASE_URL=http://localhost:12345

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@yourcompany.com
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

The API will be available at `http://localhost:12345`

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "12345:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=order_management
      - DB_USER_NAME=order_user
      - DB_USER_PASSWORD=secure_password
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: order_management
      MYSQL_USER: order_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 10s
      retries: 5
      interval: 30s
      start_period: 60s
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      timeout: 10s
      retries: 5
      interval: 30s
    restart: unless-stopped
    networks:
      - app-network

volumes:
  mysql_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

## Development Setup

### Development docker-compose.yml

Create `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "12345:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=order_management
      - DB_USER_NAME=order_user
      - DB_USER_PASSWORD=secure_password
      - ENVIRONMENT=development
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
      - /app/.venv  # Exclude virtual environment
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: order_management
      MYSQL_USER: order_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3307:3306"
    volumes:
      - mysql_dev_data:/var/lib/mysql
    networks:
      - app-network

volumes:
  mysql_dev_data:

networks:
  app-network:
    driver: bridge
```

### Development Dockerfile

Create `Dockerfile.dev`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir pytest pytest-cov pytest-asyncio

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run with auto-reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Run Development Environment

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Run in background
docker-compose -f docker-compose.dev.yml up -d --build
```

## Docker Commands

### Basic Operations

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs app
docker-compose logs -f app  # Follow logs

# Execute commands in container
docker-compose exec app bash
docker-compose exec app python -c "print('Hello')"
```

### Database Operations

```bash
# Run database migrations
docker-compose exec app alembic upgrade head

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "Migration name"

# Access database
docker-compose exec db mysql -u order_user -p order_management

# Backup database
docker-compose exec db mysqldump -u order_user -p order_management > backup.sql

# Restore database
docker-compose exec -T db mysql -u order_user -p order_management < backup.sql
```

### Development Operations

```bash
# Run tests
docker-compose exec app pytest

# Run tests with coverage
docker-compose exec app pytest --cov=app tests/

# Install new package
docker-compose exec app pip install new-package
docker-compose exec app pip freeze > requirements.txt

# Access application shell
docker-compose exec app python
```

## Production Deployment

### Production docker-compose.yml

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "80:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=order_management
      - DB_USER_NAME=order_user
      - DB_USER_PASSWORD=${DB_PASSWORD}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ENVIRONMENT=production
    env_file:
      - .env.prod
    depends_on:
      db:
        condition: service_healthy
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    networks:
      - app-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: order_management
      MYSQL_USER: order_user
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_prod_data:/var/lib/mysql
    restart: always
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - app
    restart: always
    networks:
      - app-network

volumes:
  mysql_prod_data:

networks:
  app-network:
    driver: bridge
```

### Production Dockerfile

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Use gunicorn for production
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## Monitoring and Logging

### Add Monitoring Services

```yaml
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - app-network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - app-network
```

### Centralized Logging

```yaml
# Add to docker-compose.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - app-network

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - app-network
```

## Troubleshooting

### Common Issues

1. **Port Already in Use:**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "12346:8000"  # Use different external port
   ```

2. **Database Connection Issues:**
   ```bash
   # Check database logs
   docker-compose logs db

   # Verify database is healthy
   docker-compose ps
   ```

3. **Container Build Fails:**
   ```bash
   # Clear Docker cache
   docker system prune -a

   # Rebuild without cache
   docker-compose build --no-cache
   ```

4. **Permission Issues:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Debugging

```bash
# Enter container shell
docker-compose exec app bash

# Check container logs
docker-compose logs -f app

# Inspect container
docker-compose exec app ps aux

# Check network connectivity
docker-compose exec app ping db
```

## Best Practices

1. **Use multi-stage builds for smaller images**
2. **Run containers as non-root user**
3. **Use health checks**
4. **Set resource limits**
5. **Use secrets for sensitive data**
6. **Implement proper logging**
7. **Use .dockerignore to exclude unnecessary files**
8. **Keep images updated and secure**

## Security Considerations

1. **Use official base images**
2. **Scan images for vulnerabilities**
3. **Don't store secrets in images**
4. **Use read-only containers when possible**
5. **Implement network segmentation**
6. **Regular security updates**
