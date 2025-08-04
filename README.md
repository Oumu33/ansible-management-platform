# Ansible Web Management Platform

🚀 **Professional Ansible Web Management Platform** - A comprehensive solution for managing Ansible infrastructure through a modern web interface.

## ✨ Features

- 🎯 **Simple Deployment**: SQLite-based, zero-configuration startup
- 🖥️ **Host Management**: Graphical host inventory management
- ⚡ **Task Execution**: Ad-hoc commands and Playbook execution
- 📝 **Real-time Logs**: WebSocket real-time task log streaming
- 📁 **File Management**: Playbook and configuration file management
- 🔐 **Access Control**: Role-based access control (RBAC)
- 📊 **Monitoring & Stats**: Task execution statistics and system monitoring
- 🔄 **Multi-Database**: Support for both SQLite (dev) and PostgreSQL (prod)
- 🐳 **Docker Ready**: Complete containerization with Docker Compose
- 🌐 **Modern UI**: React 18 + TypeScript + Ant Design

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **PostgreSQL**: Production database
- **SQLite**: Development database
- **Redis**: Caching and session management
- **Ansible Core**: Automation engine integration
- **WebSocket**: Real-time communication

### Frontend
- **React 18**: Modern frontend framework
- **TypeScript**: Type-safe JavaScript
- **Ant Design**: Enterprise-class UI components
- **Vite**: Next generation frontend tooling
- **Redux Toolkit**: State management

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and load balancer
- **GitHub Actions**: CI/CD pipeline

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+
- **Python** 3.11+
- **Docker** & **Docker Compose** (recommended)

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/Oumu33/ansible-management-platform.git
cd ansible-management-platform

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 2: Local Development

1. **Setup Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

2. **Setup Frontend**
```bash
cd frontend
npm install

# Start development server
npm run dev
```

3. **Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
ansible-management-platform/
├── backend/                   # FastAPI Backend Application
│   ├── app/
│   │   ├── api/              # API routes and endpoints
│   │   ├── core/             # Core configuration and utilities
│   │   ├── models/           # SQLAlchemy database models
│   │   ├── schemas/          # Pydantic data schemas
│   │   ├── services/         # Business logic services
│   │   └── middleware/       # Custom middleware
│   ├── scripts/              # Utility scripts
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                 # React Frontend Application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service calls
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript type definitions
│   ├── package.json
│   └── Dockerfile
│
├── data/                     # Data storage directory
│   ├── ansible.db           # SQLite database (development)
│   ├── files/               # File storage
│   └── logs/                # Application logs
│
├── nginx/                    # Nginx configuration
├── docker-compose.yml       # Docker orchestration
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application
DEBUG=false
SECRET_KEY=your-super-secret-key-change-in-production

# Database (PostgreSQL for production)
POSTGRES_DB=ansible_web
POSTGRES_USER=ansible_user  
POSTGRES_PASSWORD=secure_password_here

# Redis
REDIS_PASSWORD=redis_secure_password

# Security
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_HOSTS=["http://localhost:3000","https://yourdomain.com"]

# OAuth2 (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### Database Configuration

The platform supports both SQLite (development) and PostgreSQL (production):

- **Development**: Uses SQLite database stored in `data/ansible.db`
- **Production**: Uses PostgreSQL with connection pooling and migrations

## 🗄️ Database Schema

Key database tables:

- **users**: User management and authentication
- **hosts**: Ansible host inventory
- **host_groups**: Host grouping and organization  
- **tasks**: Task execution history and status
- **playbooks**: Playbook management and storage
- **file_metadata**: File system metadata
- **audit_logs**: Security and operation audit logs

## 📚 API Documentation

After starting the backend server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Important**: Change the default password immediately in production!

## 🛠️ Development Guide

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Code formatting
black app/

# Code linting
flake8 app/
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Code linting
npm run lint

# Type checking
npm run type-check
```

## 🐳 Docker Deployment

### Development Environment

```bash
# Start all services
docker-compose up -d

# View service status
docker-compose ps

# View logs
docker-compose logs -f [service_name]

# Stop services
docker-compose down
```

### Production Environment

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d

# Scale backend services
docker-compose up -d --scale backend=3
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Fine-grained permission system
- **Rate Limiting**: API rate limiting and DDoS protection
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **HTTPS Support**: SSL/TLS encryption ready
- **CORS Configuration**: Configurable cross-origin policies
- **OAuth2 Integration**: Support for external authentication providers

## 📊 Monitoring & Logging

- **Application Logs**: Structured logging with different levels
- **Access Logs**: HTTP request/response logging
- **Audit Logs**: Security and operation audit trail
- **Performance Metrics**: Built-in performance monitoring
- **Health Checks**: Docker health check endpoints

## 🚀 Production Deployment

### System Requirements

- **CPU**: 2+ cores
- **RAM**: 4GB+ recommended
- **Storage**: 20GB+ for logs and data
- **Network**: Stable internet connection

### Deployment Steps

1. **Server Preparation**
```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and configure
git clone https://github.com/Oumu33/ansible-management-platform.git
cd ansible-management-platform
cp .env.example .env
# Edit .env with production values
```

2. **SSL/TLS Setup**
```bash
# Generate SSL certificates or use Let's Encrypt
# Place certificates in nginx/ssl/
```

3. **Start Production Services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. **Initialize Database**
```bash
docker-compose exec backend python scripts/init_db.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Issues

- **Documentation**: [Wiki](https://github.com/Oumu33/ansible-management-platform/wiki)
- **Issues**: [GitHub Issues](https://github.com/Oumu33/ansible-management-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Oumu33/ansible-management-platform/discussions)

## 🎯 Roadmap

- [ ] **Multi-tenancy**: Support for multiple organizations
- [ ] **Advanced Scheduling**: Cron-like task scheduling
- [ ] **Vault Integration**: HashiCorp Vault integration
- [ ] **Kubernetes Support**: Native Kubernetes deployment
- [ ] **Grafana Integration**: Advanced monitoring dashboards
- [ ] **Mobile App**: React Native mobile application
- [ ] **Plugin System**: Extensible plugin architecture

---

**Built with ❤️ using FastAPI + React + TypeScript**

**⭐ Star this repo if you find it useful!**