# E-Commerce Microservices Application - DevOps Deployment

## Overview
This is a complete microservices application built for DevOps deployment practice using Jenkins CI/CD, Docker, Kubernetes, and AWS EKS with Ingress Controller.

## Architecture
- **Frontend**: HTML/JavaScript gateway
- **User Service**: User management and authentication
- **Product Service**: Product catalog and inventory
- **Order Service**: Order processing and management
- **Payment Service**: Payment processing
- **Notification Service**: Notifications and alerts
- **Database**: MongoDB container

## Port Configuration
- Frontend: 3000
- User Service: 3001
- Product Service: 3002
- Order Service: 3003
- Payment Service: 3004
- Notification Service: 3005
- MongoDB: 27017

## Prerequisites
- Jenkins running on port 8080
- Docker configured in Jenkins (tool name: docker)
- DockerHub credentials configured as 'dockerhub-creds'
- AWS credentials configured as 'aws-creds'
- AWS EKS cluster 'kastro-eks' in us-east-1
- kubectl configured

## Local Development Setup

### 1. Clone and Run with Docker Compose
```bash
git clone <your-repo-url>
cd microservices-app
docker-compose up -d
```

### 2. Access MongoDB
```bash
# Connect to MongoDB container
docker exec -it mongodb mongo

# Use the application database
use ecommerce_db

# View collections
show collections

# Query users
db.users.find()

# Query products
db.products.find()

# Query orders
db.orders.find()
```

### 3. Access Application
- Frontend: http://localhost:3000
- Admin Dashboard: http://localhost:3000/admin

## Jenkins CI/CD Setup

### 1. Create Jenkins Pipeline Jobs
Create separate pipeline jobs for each service:
- `user-service-pipeline`
- `product-service-pipeline`
- `order-service-pipeline`
- `payment-service-pipeline`
- `notification-service-pipeline`
- `frontend-pipeline`

### 2. Configure Build Parameters
For each job, add these parameters:
- **IMAGE_TAG**: String parameter (default: latest)
- **DEPLOY_ENV**: Choice parameter (dev, staging, prod)

### 3. Pipeline Configuration
- Source: SCM (Git)
- Script Path: [service-name]/Jenkinsfile
- Build Trigger: GitHub webhook or manual

## Kubernetes Deployment

### 1. Setup EKS Cluster
```bash
# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name kastro-eks

# Verify connection
kubectl get nodes
```

### 2. Deploy MongoDB
```bash
kubectl apply -f k8s/mongodb/
```

### 3. Deploy Services
```bash
# Deploy all services
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
```

### 4. Setup Ingress Controller
```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml

# Apply ingress configuration
kubectl apply -f k8s/ingress.yml
```

### 5. Get Application URL
```bash
# Get Load Balancer URL
kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

## Application Features

### Admin Dashboard
- **Users**: Add/view user profiles
- **Products**: Add/manage product catalog
- **Orders**: View and manage orders
- **Payments**: Monitor payment transactions
- **Notifications**: Send system notifications

### User Features
- Browse products
- Place orders
- View order history
- Receive notifications

## Monitoring and Troubleshooting

### Check Service Status
```bash
# Check all pods
kubectl get pods

# Check service logs
kubectl logs -l app=user-service
kubectl logs -l app=product-service
kubectl logs -l app=order-service
kubectl logs -l app=payment-service
kubectl logs -l app=notification-service
```

### Debug Issues
```bash
# Describe pod for detailed info
kubectl describe pod <pod-name>

# Check ingress status
kubectl describe ingress microservices-ingress

# Check service endpoints
kubectl get endpoints
```

## Deployment Workflow

1. **Code Push**: Developer pushes code to repository
2. **Jenkins Trigger**: Webhook triggers Jenkins pipeline
3. **Build**: Jenkins builds Docker image
4. **Push**: Image pushed to DockerHub
5. **Deploy**: Jenkins deploys to EKS cluster
6. **Verify**: Health checks and monitoring

## Security Considerations

- MongoDB credentials stored in Kubernetes secrets
- Docker images scanned for vulnerabilities
- RBAC configured for service accounts
- Network policies for service communication

## Scaling

```bash
# Scale services
kubectl scale deployment user-service --replicas=3
kubectl scale deployment product-service --replicas=3
```

## Backup and Recovery

```bash
# Backup MongoDB
kubectl exec -it mongodb-pod -- mongodump --out /backup

# Restore MongoDB
kubectl exec -it mongodb-pod -- mongorestore /backup
```

## Support

For issues and questions:
1. Check service logs
2. Verify ingress configuration
3. Check MongoDB connectivity
4. Review Jenkins build logs