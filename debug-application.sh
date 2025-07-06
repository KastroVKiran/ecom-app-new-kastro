#!/bin/bash

echo "🔍 E-Commerce Application Debug Script"
echo "======================================"

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists kubectl; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

echo "📋 Comprehensive Application Debug Information"
echo ""

echo "1. 🏗️  EKS Cluster Information:"
echo "--------------------------------"
kubectl cluster-info
echo ""

echo "2. 🖥️  Cluster Nodes:"
echo "-------------------"
kubectl get nodes -o wide
echo ""

echo "3. 🔌 NGINX Ingress Controller Status:"
echo "------------------------------------"
kubectl get pods -n ingress-nginx
echo ""
kubectl get svc -n ingress-nginx
echo ""

echo "4. 🚀 Application Pods Status:"
echo "-----------------------------"
kubectl get pods -o wide
echo ""

echo "5. 🌐 Application Services:"
echo "-------------------------"
kubectl get svc
echo ""

echo "6. 🔗 Ingress Configuration:"
echo "---------------------------"
kubectl get ingress
echo ""
kubectl describe ingress microservices-ingress
echo ""

echo "7. 📊 Pod Resource Usage:"
echo "------------------------"
kubectl top pods 2>/dev/null || echo "Metrics server not available"
echo ""

echo "8. 📝 Recent Events:"
echo "------------------"
kubectl get events --sort-by=.metadata.creationTimestamp | tail -20
echo ""

echo "9. 🔍 Application URLs:"
echo "---------------------"
LB_URL=$(kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null)

if [ -z "$LB_URL" ]; then
    echo "⏳ Load Balancer URL not ready yet."
    echo "   This usually takes 2-5 minutes after deployment."
    echo ""
    echo "🔄 To check again later, run:"
    echo "   kubectl get ingress microservices-ingress"
else
    echo "✅ Application is ready!"
    echo ""
    echo "🌐 Main URLs:"
    echo "   Main Application: http://$LB_URL/"
    echo "   Admin Dashboard:  http://$LB_URL/admin"
    echo ""
    echo "🔧 Service URLs:"
    echo "   User Service:         http://$LB_URL/user-service"
    echo "   Product Service:      http://$LB_URL/product-service"
    echo "   Order Service:        http://$LB_URL/order-service"
    echo "   Payment Service:      http://$LB_URL/payment-service"
    echo "   Notification Service: http://$LB_URL/notification-service"
fi

echo ""
echo "10. 🩺 Health Check Commands:"
echo "----------------------------"
echo "To check individual service health:"
echo "kubectl logs -l app=frontend"
echo "kubectl logs -l app=user-service"
echo "kubectl logs -l app=product-service"
echo "kubectl logs -l app=order-service"
echo "kubectl logs -l app=payment-service"
echo "kubectl logs -l app=notification-service"
echo "kubectl logs -l app=mongodb"
echo ""

echo "11. 🔧 Troubleshooting Commands:"
echo "-------------------------------"
echo "If application is not accessible:"
echo "1. Check ingress controller: kubectl get pods -n ingress-nginx"
echo "2. Check load balancer: kubectl get svc -n ingress-nginx"
echo "3. Port forward for testing: kubectl port-forward service/frontend 8080:3000"
echo "4. Check pod logs: kubectl logs <pod-name>"
echo "5. Restart deployment: kubectl rollout restart deployment/<service-name>"
echo ""

# Check if any pods are not running
echo "12. 🚨 Pod Status Summary:"
echo "------------------------"
NOT_RUNNING=$(kubectl get pods --no-headers | grep -v Running | grep -v Completed)
if [ -z "$NOT_RUNNING" ]; then
    echo "✅ All pods are running successfully!"
else
    echo "⚠️  Some pods are not running:"
    echo "$NOT_RUNNING"
    echo ""
    echo "🔍 Check logs for failed pods using:"
    echo "kubectl logs <pod-name>"
    echo "kubectl describe pod <pod-name>"
fi

echo ""
echo "🎯 Debug completed! If you need help, share this output."