# SysInsight - Real-time Linux System Monitoring

SysInsight is a containerized web application for real-time Linux system performance monitoring with an intuitive dashboard interface.

## Features

- **Real-time Monitoring**: Live CPU, memory, and disk usage tracking
- **RESTful API**: Clean API endpoints for metrics data
- **Interactive Dashboard**: Beautiful Chart.js visualizations
- **Configurable Alerts**: Customizable warning and critical thresholds
- **Docker Support**: Fully containerized for easy deployment
- **Production Ready**: Gunicorn WSGI server with health checks

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ and pip

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sysinsight.git
cd sysinsight
```

2. Copy environment configuration:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Build and run:
```bash
docker-compose up -d
```

4. Access the dashboard:
```
http://localhost:5000
```

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
cp .env.example .env
export FLASK_ENV=development
```

4. Run application:
```bash
python run.py
```

## API Endpoints

### Metrics Endpoints

- `GET /api/metrics/cpu` - CPU usage metrics
- `GET /api/metrics/memory` - Memory usage metrics
- `GET /api/metrics/disk` - Disk usage metrics
- `GET /api/metrics/all` - All system metrics

### Health Endpoints

- `GET /health` or `/healthz` - Basic health check
- `GET /ready` or `/readyz` - Readiness check with system validation

## Configuration

Configure SysInsight via environment variables in `.env`:

```bash
# Monitoring intervals (seconds)
METRICS_INTERVAL=5

# Alert thresholds (percentage)
CPU_WARNING=70
CPU_CRITICAL=85
MEMORY_WARNING=75
MEMORY_CRITICAL=90

# Enable features
ENABLE_ALERTS=true
```

## Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

## Production Deployment

1. Set production environment:
```bash
FLASK_ENV=production
SECRET_KEY=your-secure-random-key
```

2. Use provided Docker configuration with resource limits
3. Configure reverse proxy (Nginx recommended) for SSL/TLS
4. Set up log aggregation and monitoring
5. Enable automatic restarts with container orchestration

## Architecture

- **Backend**: Flask 3.1.2 with psutil for system metrics
- **Frontend**: Vanilla JavaScript with Chart.js 4.4.0
- **Server**: Gunicorn with multiple workers
- **Container**: Multi-stage Docker build with security hardening

## Security Best Practices

- Non-root container user
- Minimal base image (python:3.11-slim)
- No secrets in images
- Health checks for container orchestration
- CORS configuration
- Input validation

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please open a GitHub issue.
