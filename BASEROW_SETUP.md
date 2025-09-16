# Baserow Local Setup Guide

This guide will help you set up a local Baserow instance using Docker for your Spreadsheet Consolidator tool.

## Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.7+ environment

## Quick Start

### 1. Start Baserow Services

```bash
# From the project root directory
docker-compose up -d

# Check if services are running
docker-compose ps
```

This will start:
- **Baserow**: Main application at http://localhost:8080
- **PostgreSQL**: Database backend
- **Redis**: Caching and session storage

### 2. Access Baserow

1. Open your browser and go to `http://localhost:8080`
2. Create your admin account (first user becomes admin)
3. Create a workspace and database
4. Note down your API token from Settings > API tokens

### 3. Get Connection Details

You'll need these details for the Spreadsheet Consolidator:
- **Base URL**: `http://localhost:8080`
- **API Token**: Generated from Baserow Settings
- **Table ID**: Found in the URL when viewing your table

## Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f baserow

# Restart services
docker-compose restart

# Update Baserow
docker-compose pull
docker-compose up -d
```

## Backup and Restore

### Backup
```bash
# Create backup
docker-compose exec postgres pg_dump -U baserow baserow > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup volumes
docker run --rm -v spreadsheet_consolidator_baserow_data:/data -v $(pwd):/backup alpine tar czf /backup/baserow_data_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

### Restore
```bash
# Restore database
cat backup_file.sql | docker-compose exec -T postgres psql -U baserow -d baserow
```

## Configuration

The Docker Compose setup includes:
- Persistent data storage
- Automatic container restart
- Network isolation
- Custom container names for easy management

## Troubleshooting

### Port Conflicts
If port 8080 is already in use, change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8081:80"  # Change 8080 to 8081
```

### Reset Everything
```bash
docker-compose down -v
docker-compose up -d
```
This will remove all data and start fresh.

## Integration with Spreadsheet Consolidator

Once Baserow is running, use the sidebar in the Spreadsheet Consolidator app to connect:
1. Base URL: `http://localhost:8080`
2. API Token: From Baserow Settings
3. Table ID: From your table URL

The integration supports:
- Automatic field creation
- Batch data upload
- Data type detection
- Progress tracking
- Error handling
