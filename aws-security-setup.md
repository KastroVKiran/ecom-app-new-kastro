# AWS Security Groups and Application Access Guide

## 🔐 Required Security Group Configurations

### 1. EKS Worker Nodes Security Group

Your EKS worker nodes need these **INBOUND** rules:

```
Port Range    Protocol    Source                    Description
22            TCP         Your IP/CIDR              SSH access
80            TCP         0.0.0.0/0                HTTP traffic
443           TCP         0.0.0.0/0                HTTPS traffic
30000-32767   TCP         0.0.0.0/0                NodePort range
10250         TCP         EKS Control Plane SG     Kubelet API
```

**OUTBOUND** rules:
```
Port Range    Protocol    Destination               Description
All           All         0.0.0.0/0                All outbound traffic
```

### 2. EKS Control Plane Security Group

**INBOUND** rules:
```
Port Range    Protocol    Source                    Description
443           TCP         Worker Nodes SG          HTTPS API server
443           TCP         Your IP/CIDR              kubectl access
```

### 3. Load Balancer Security Group (Auto-created by NGINX Ingress)

The NGINX Ingress Controller will automatically create a Classic Load Balancer with these rules:

**INBOUND** rules:
```
Port Range    Protocol    Source                    Description
80            TCP         0.0.0.0/0                HTTP traffic
443           TCP         0.0.0.0/0                HTTPS traffic
```

## 🔍 Troubleshooting Steps

### Step 1: Check NGINX Ingress Controller Installation

```bash
# Check if NGINX Ingress Controller is running
kubectl get pods -n ingress-nginx

# Expected output should show running pods like:
# ingress-nginx-controller-xxx
# ingress-nginx-admission-create-xxx
# ingress-nginx-admission-patch-xxx
```

### Step 2: Verify Load Balancer Creation

```bash
# Check if Load Balancer is created
kubectl get svc -n ingress-nginx

# Look for service type LoadBalancer with EXTERNAL-IP
# Example output:
# NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)
# ingress-nginx-controller             LoadBalancer   10.100.xxx.xxx  a1234567890abcdef-1234567890.us-east-1.elb.amazonaws.com              80:31234/TCP,443:31567/TCP
```

### Step 3: Check Your Ingress Resource

```bash
# Check ingress status
kubectl get ingress microservices-ingress

# Describe ingress for detailed info
kubectl describe ingress microservices-ingress

# Expected output should show:
# Address: <load-balancer-dns-name>
# Rules with proper backend services
```

### Step 4: Verify Application Pods

```bash
# Check all pods are running
kubectl get pods

# All pods should be in "Running" status
# If any pod is not running, check logs:
kubectl logs <pod-name>
```

## 🚀 Correct Application Access URLs

After successful deployment, access your application using:

### Main Application URLs
```
Main App:        http://<LOAD-BALANCER-DNS>/
Admin Dashboard: http://<LOAD-BALANCER-DNS>/admin
```

### Individual Service URLs (for testing)
```
User Service:         http://<LOAD-BALANCER-DNS>/user-service
Product Service:      http://<LOAD-BALANCER-DNS>/product-service  
Order Service:        http://<LOAD-BALANCER-DNS>/order-service
Payment Service:      http://<LOAD-BALANCER-DNS>/payment-service
Notification Service: http://<LOAD-BALANCER-DNS>/notification-service
```

## 🔧 Fix Common Issues

### Issue 1: Ingress Controller Not Working

If you installed the wrong version for EKS 1.30, reinstall with the correct version:

```bash
# Remove old ingress controller
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/aws/deploy.yaml

# Install correct version for EKS 1.30
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml

# Wait for deployment
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### Issue 2: Load Balancer Not Getting External IP

```bash
# Check load balancer service
kubectl get svc -n ingress-nginx ingress-nginx-controller

# If EXTERNAL-IP shows <pending>, check:
# 1. AWS credentials are correct
# 2. EKS cluster has proper IAM roles
# 3. Subnets are properly tagged
```

### Issue 3: Application Not Responding

```bash
# Test internal connectivity
kubectl port-forward service/frontend 8080:3000

# Then access: http://localhost:8080
# If this works, the issue is with ingress configuration
```

## 📋 Complete Verification Checklist

Run these commands to verify everything is working:

```bash
# 1. Check cluster nodes
kubectl get nodes
# All nodes should be "Ready"

# 2. Check ingress controller
kubectl get pods -n ingress-nginx
# All pods should be "Running"

# 3. Check your application pods
kubectl get pods
# All application pods should be "Running"

# 4. Check services
kubectl get svc
# All services should have ClusterIP assigned

# 5. Check ingress
kubectl get ingress
# Should show ADDRESS with load balancer DNS

# 6. Get the application URL
kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

## 🌐 Final Application Access

Once everything is working, you should be able to access:

1. **Main Application**: `http://<LOAD-BALANCER-DNS>/`
   - This shows the homepage with navigation to all services

2. **Admin Dashboard**: `http://<LOAD-BALANCER-DNS>/admin`
   - Central admin panel to manage all services

3. **Individual Services**: Click on navigation menu items
   - Each service has its own admin interface
   - URLs update automatically when navigating

## 🔄 If Still Not Working

If you're still having issues, run this comprehensive debug script:

```bash
#!/bin/bash
echo "=== EKS Cluster Debug Information ==="

echo "1. Cluster Info:"
kubectl cluster-info

echo "2. Nodes:"
kubectl get nodes -o wide

echo "3. Ingress Controller:"
kubectl get pods -n ingress-nginx

echo "4. Ingress Controller Service:"
kubectl get svc -n ingress-nginx

echo "5. Application Pods:"
kubectl get pods -o wide

echo "6. Application Services:"
kubectl get svc

echo "7. Ingress Resource:"
kubectl get ingress
kubectl describe ingress microservices-ingress

echo "8. Recent Events:"
kubectl get events --sort-by=.metadata.creationTimestamp | tail -20

echo "9. Load Balancer URL:"
LB_URL=$(kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Application URL: http://$LB_URL"
echo "Admin Dashboard: http://$LB_URL/admin"
```

Save this as `debug.sh`, make it executable (`chmod +x debug.sh`), and run it to get complete diagnostic information.