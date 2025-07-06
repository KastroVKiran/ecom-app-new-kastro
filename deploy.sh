#!/bin/bash

# E-Commerce Microservices Deployment Script
# This script helps with local development and testing

set -e

echo "🚀 E-Commerce Microservices Deployment Script"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Function to start local development
start_local() {
    echo "🏠 Starting local development environment..."
    docker-compose down
    docker-compose up -d
    
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    echo "🌐 Application URLs:"
    echo "Frontend: http://localhost:3000"
    echo "Admin Dashboard: http://localhost:3000/admin"
    echo "User Service: http://localhost:3001"
    echo "Product Service: http://localhost:3002"
    echo "Order Service: http://localhost:3003"
    echo "Payment Service: http://localhost:3004"
    echo "Notification Service: http://localhost:3005"
    echo "MongoDB: localhost:27017"
}

# Function to stop local development
stop_local() {
    echo "🛑 Stopping local development environment..."
    docker-compose down
    echo "✅ Local environment stopped!"
}

# Function to build all images
build_images() {
    echo "🔨 Building all Docker images..."
    
    services=("frontend" "user-service" "product-service" "order-service" "payment-service" "notification-service")
    
    for service in "${services[@]}"; do
        echo "Building $service..."
        docker build -t kastrov/$service:latest ./$service/
    done
    
    echo "✅ All images built successfully!"
}

# Function to push all images
push_images() {
    echo "📤 Pushing all Docker images to DockerHub..."
    
    services=("frontend" "user-service" "product-service" "order-service" "payment-service" "notification-service")
    
    for service in "${services[@]}"; do
        echo "Pushing kastrov/$service:latest..."
        docker push kastrov/$service:latest
    done
    
    echo "✅ All images pushed successfully!"
}

# Function to access MongoDB
access_mongodb() {
    echo "🗄️ Accessing MongoDB..."
    echo "Connecting to MongoDB container..."
    
    if docker ps | grep -q mongodb; then
        echo "MongoDB commands:"
        echo "docker exec -it mongodb mongo"
        echo "use ecommerce_db"
        echo "show collections"
        echo "db.users.find()"
        echo ""
        docker exec -it mongodb mongo
    else
        echo "❌ MongoDB container is not running. Start the local environment first."
    fi
}

# Function to show logs
show_logs() {
    echo "📋 Showing application logs..."
    docker-compose logs -f
}

# Function to clean up
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose down -v
    docker system prune -f
    echo "✅ Cleanup completed!"
}

# Main menu
case "${1:-}" in
    "start")
        start_local
        ;;
    "stop")
        stop_local
        ;;
    "build")
        build_images
        ;;
    "push")
        push_images
        ;;
    "mongo")
        access_mongodb
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        cleanup
        ;;
    *)
        echo "Usage: $0 {start|stop|build|push|mongo|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  start  - Start local development environment"
        echo "  stop   - Stop local development environment"
        echo "  build  - Build all Docker images"
        echo "  push   - Push all images to DockerHub"
        echo "  mongo  - Access MongoDB container"
        echo "  logs   - Show application logs"
        echo "  clean  - Clean up containers and images"
        echo ""
        echo "Examples:"
        echo "  ./deploy.sh start"
        echo "  ./deploy.sh mongo"
        echo "  ./deploy.sh build && ./deploy.sh push"
        exit 1
        ;;
esac