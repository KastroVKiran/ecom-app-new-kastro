#!/bin/bash

echo "🔧 Fixing NGINX Ingress Controller for EKS 1.30"
echo "================================================"

# Remove old ingress controller if exists
echo "1. Removing old ingress controller..."
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/aws/deploy.yaml --ignore-not-found=true

# Wait a moment for cleanup
echo "2. Waiting for cleanup..."
sleep 10

# Install correct version for EKS 1.30
echo "3. Installing correct NGINX Ingress Controller for EKS 1.30..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml

# Wait for ingress controller to be ready
echo "4. Waiting for ingress controller to be ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

# Check status
echo "5. Checking ingress controller status..."
kubectl get pods -n ingress-nginx

echo "6. Checking load balancer service..."
kubectl get svc -n ingress-nginx

# Apply your ingress resource
echo "7. Applying application ingress..."
kubectl apply -f k8s/ingress.yml

# Wait a moment for ingress to be processed
echo "8. Waiting for ingress to be ready..."
sleep 30

# Get the application URL
echo "9. Getting application URL..."
LB_URL=$(kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

if [ -z "$LB_URL" ]; then
    echo "⏳ Load balancer URL not ready yet. Please wait a few minutes and run:"
    echo "kubectl get ingress microservices-ingress"
else
    echo "✅ Application is ready!"
    echo "🌐 Main Application: http://$LB_URL/"
    echo "🔧 Admin Dashboard: http://$LB_URL/admin"
fi

echo ""
echo "📋 To check status later, run:"
echo "kubectl get ingress microservices-ingress"
echo "kubectl get svc -n ingress-nginx"