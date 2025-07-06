# 🚀 Complete E-Commerce Microservices Deployment Guide

## 🎯 Quick Start

### 1. Run the Jenkins Pipeline
1. **Trigger the pipeline** with these parameters:
   - IMAGE_TAG: `v1.0`
   - DEPLOY_ENV: `dev`
   - DEPLOY_TYPE: `all`

2. **Wait for completion** (approximately 10-15 minutes)

3. **Get your application URL** from the pipeline output

### 2. Access Your Application
```
Main Application: http://<LOAD-BALANCER-DNS>/
Admin Dashboard:  http://<LOAD-BALANCER-DNS>/admin
```

## 🔐 AWS Security Groups Setup

### EKS Worker Nodes Security Group - INBOUND Rules:
```
Port 22         - Source: Your IP/CIDR        (SSH access)
Port 80         - Source: 0.0.0.0/0          (HTTP traffic)
Port 443        - Source: 0.0.0.0/0          (HTTPS traffic)
Port 30000-32767 - Source: 0.0.0.0/0         (NodePort range)
```

### Load Balancer Security Group (Auto-created):
```
Port 80         - Source: 0.0.0.0/0          (HTTP traffic)
Port 443        - Source: 0.0.0.0/0          (HTTPS traffic)
```

## 🔧 What the Pipeline Does

### Stage 1: Build Individual Services
- ✅ **Frontend Service** - Web interface
- ✅ **User Service** - User management
- ✅ **Product Service** - Product catalog
- ✅ **Order Service** - Order processing
- ✅ **Payment Service** - Payment handling
- ✅ **Notification Service** - Notifications

### Stage 2: Deploy to Kubernetes
- Deploys MongoDB database
- Deploys all microservices
- Creates Kubernetes services

### Stage 3: Fix Ingress Controller
- Removes incompatible ingress controller
- Installs correct version for EKS 1.30
- Waits for readiness

### Stage 4: Deploy Application Ingress
- Applies fixed ingress configuration
- Routes traffic to correct services

### Stage 5: Verification
- Checks all deployments
- Verifies pod status
- Gets application URL

## 🌐 Application Features

### Main Application (`/`)
- Beautiful homepage with service overview
- Navigation to all microservices
- Real-time status indicators

### Admin Dashboard (`/admin`)
- Central management interface
- System status monitoring
- Quick access to all services

### Individual Services
- **User Service** (`/user-service`) - User management
- **Product Service** (`/product-service`) - Product catalog
- **Order Service** (`/order-service`) - Order processing
- **Payment Service** (`/payment-service`) - Payment handling
- **Notification Service** (`/notification-service`) - Notifications

## 🔍 Troubleshooting

### If Application Shows 404 Error:

1. **Check Ingress Controller**:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

2. **Check Load Balancer**:
   ```bash
   kubectl get svc -n ingress-nginx
   ```

3. **Check Application Pods**:
   ```bash
   kubectl get pods
   ```

4. **Check Ingress Status**:
   ```bash
   kubectl get ingress microservices-ingress
   ```

### If Load Balancer URL Not Ready:
- Wait 2-5 minutes for AWS Load Balancer provisioning
- Check AWS Console for Load Balancer status
- Verify security groups are correctly configured

### If Services Not Responding:
```bash
# Check pod logs
kubectl logs -l app=frontend
kubectl logs -l app=user-service

# Port forward for testing
kubectl port-forward service/frontend 8080:3000
```

## 📊 Monitoring Commands

```bash
# Check all resources
kubectl get all

# Check ingress details
kubectl describe ingress microservices-ingress

# Check recent events
kubectl get events --sort-by=.metadata.creationTimestamp | tail -20

# Check resource usage
kubectl top pods
```

## 🗄️ MongoDB Access

```bash
# Connect to MongoDB
kubectl exec -it $(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}') -- mongo

# Use the database
use ecommerce_db

# View collections
show collections

# Query data
db.users.find()
db.products.find()
db.orders.find()
```

## 🔄 Scaling Services

```bash
# Scale individual services
kubectl scale deployment frontend --replicas=3
kubectl scale deployment user-service --replicas=2
kubectl scale deployment product-service --replicas=2
```

## 🚀 Production Deployment

For production deployment:

1. **Update parameters**:
   - IMAGE_TAG: `v1.0-prod`
   - DEPLOY_ENV: `prod`
   - DEPLOY_TYPE: `all`

2. **Additional considerations**:
   - Use managed MongoDB (AWS DocumentDB)
   - Enable HTTPS with SSL certificates
   - Configure monitoring and logging
   - Set up backup strategies

## 🎉 Success Indicators

✅ **Pipeline completes successfully**
✅ **All pods are in "Running" status**
✅ **Ingress has external IP/hostname**
✅ **Application accessible via browser**
✅ **All navigation links work**
✅ **Admin dashboards functional**

## 📞 Support

If you encounter issues:

1. **Check the pipeline logs** in Jenkins
2. **Run the debug commands** provided above
3. **Verify AWS security groups** are correctly configured
4. **Ensure EKS cluster** has proper permissions
5. **Check load balancer** status in AWS Console

## 🎯 Expected Results

After successful deployment:
- **Main application** loads with beautiful interface
- **Navigation works** between all services
- **Admin dashboards** are accessible and functional
- **URLs update automatically** when navigating
- **All microservices** respond correctly
- **MongoDB** stores data persistently

Your E-Commerce Microservices application is now ready for production use! 🎉
