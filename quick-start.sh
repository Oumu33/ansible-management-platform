#!/bin/bash

# Ansible Web Management Platform Quick Start Script
# Author: Development Team
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. Consider using a regular user account."
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check system dependencies
check_dependencies() {
    log_info "Checking system dependencies..."
    
    local missing_deps=()
    
    # Check Docker
    if ! command -v docker >/dev/null 2>&1; then
        missing_deps+=("docker")
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
        missing_deps+=("docker-compose")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install Docker and Docker Compose manually."
        exit 1
    else
        log_success "All dependencies installed"
    fi
}

# Setup environment configuration
setup_environment() {
    log_info "Setting up environment configuration..."
    
    if [[ ! -f .env ]]; then
        if [[ -f .env.example ]]; then
            cp .env.example .env
            log_info "Created .env file from .env.example"
        else
            log_warning ".env.example file not found, creating basic .env file"
            cat > .env << EOF
NODE_ENV=production
POSTGRES_PASSWORD=secure_postgres_password_$(openssl rand -hex 8)
REDIS_PASSWORD=secure_redis_password_$(openssl rand -hex 8)
SECRET_KEY=$(openssl rand -base64 32)
GRAFANA_ADMIN_PASSWORD=grafana_$(openssl rand -hex 4)
EOF
        fi
        
        log_warning "Please edit .env file and set appropriate passwords and configuration"
        log_info "Generated random passwords have been saved in .env file"
    else
        log_success "Environment configuration file exists"
    fi
}

# Deploy services
deploy_services() {
    log_info "Starting service deployment..."
    
    # Create necessary directories
    mkdir -p logs nginx/ssl data/{files/{config,inventory,playbooks},logs}
    
    # Start services
    log_info "Starting services..."
    docker-compose up -d
    
    log_success "Service deployment completed"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to start..."
    
    local max_attempts=60
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            log_success "Services are ready"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done
    
    log_error "Service startup timeout"
    return 1
}

# Display deployment information
show_deployment_info() {
    log_success "Deployment completed!"
    echo
    echo "===================================="
    echo "  Ansible Web Management Platform  "
    echo "===================================="
    echo
    echo "Service Access URLs:"
    echo "  Frontend:        http://localhost:3000"
    echo "  Backend API:     http://localhost:8000"
    echo "  API Docs:        http://localhost:8000/docs"
    echo "  ReDoc:           http://localhost:8000/redoc"
    echo
    echo "Default Credentials:"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo
    echo "Common Commands:"
    echo "  View service status:  docker-compose ps"
    echo "  View logs:            docker-compose logs -f [service_name]"
    echo "  Stop services:        docker-compose down"
    echo "  Restart services:     docker-compose restart"
    echo
    echo "Documentation:"
    echo "  README.md:            Project documentation"
    echo "  logs/:                Log files directory"
    echo "  data/:                Data storage directory"
    echo
}

# Main function
main() {
    echo "=========================================="
    echo "  Ansible Web Management Platform Setup  "
    echo "=========================================="
    echo
    
    check_root
    check_dependencies
    setup_environment
    deploy_services
    
    if wait_for_services; then
        show_deployment_info
    else
        log_warning "Deployment completed, but some services may need additional configuration"
        log_info "Please check 'docker-compose logs' for detailed information"
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi