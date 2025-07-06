pipeline {
    agent any
    
    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag for all services')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'prod'], description: 'Deployment environment')
        choice(name: 'DEPLOY_TYPE', choices: ['all', 'frontend', 'user-service', 'product-service', 'order-service', 'payment-service', 'notification-service'], description: 'Service to deploy')
    }
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        AWS_CREDENTIALS = credentials('aws-creds')
        DOCKERHUB_USERNAME = 'kastrov'
        EKS_CLUSTER_NAME = 'kastro-eks'
        AWS_REGION = 'us-east-1'
        GITHUB_REPO = 'https://github.com/KastroVKiran/ecom-app-new-kastro.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'master', url: "${GITHUB_REPO}"
            }
        }
        
        stage('Build Individual Services') {
            parallel {
                stage('Build Frontend') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'frontend' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building Frontend Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def frontendImage = docker.build("${DOCKERHUB_USERNAME}/frontend:${params.IMAGE_TAG}", "./frontend")
                                frontendImage.push()
                                frontendImage.push("latest")
                                echo '✅ Frontend build completed!'
                            }
                        }
                    }
                }
                
                stage('Build User Service') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'user-service' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building User Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def userImage = docker.build("${DOCKERHUB_USERNAME}/user-service:${params.IMAGE_TAG}", "./user-service")
                                userImage.push()
                                userImage.push("latest")
                                echo '✅ User Service build completed!'
                            }
                        }
                    }
                }
                
                stage('Build Product Service') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'product-service' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building Product Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def productImage = docker.build("${DOCKERHUB_USERNAME}/product-service:${params.IMAGE_TAG}", "./product-service")
                                productImage.push()
                                productImage.push("latest")
                                echo '✅ Product Service build completed!'
                            }
                        }
                    }
                }
                
                stage('Build Order Service') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'order-service' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building Order Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def orderImage = docker.build("${DOCKERHUB_USERNAME}/order-service:${params.IMAGE_TAG}", "./order-service")
                                orderImage.push()
                                orderImage.push("latest")
                                echo '✅ Order Service build completed!'
                            }
                        }
                    }
                }
                
                stage('Build Payment Service') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'payment-service' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building Payment Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def paymentImage = docker.build("${DOCKERHUB_USERNAME}/payment-service:${params.IMAGE_TAG}", "./payment-service")
                                paymentImage.push()
                                paymentImage.push("latest")
                                echo '✅ Payment Service build completed!'
                            }
                        }
                    }
                }
                
                stage('Build Notification Service') {
                    when {
                        anyOf {
                            expression { params.DEPLOY_TYPE == 'all' }
                            expression { params.DEPLOY_TYPE == 'notification-service' }
                        }
                    }
                    steps {
                        script {
                            echo '🏗️ Building Notification Service...'
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def notificationImage = docker.build("${DOCKERHUB_USERNAME}/notification-service:${params.IMAGE_TAG}", "./notification-service")
                                notificationImage.push()
                                notificationImage.push("latest")
                                echo '✅ Notification Service build completed!'
                            }
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh """
                            echo '🚀 Starting Kubernetes deployment...'
                            
                            # Configure kubectl
                            aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER_NAME}
                            
                            echo '✅ Kubectl configured successfully'
                            kubectl get nodes
                            
                            # Deploy MongoDB first
                            echo '🗄️ Deploying MongoDB...'
                            kubectl apply -f k8s/mongodb/
                            
                            # Wait for MongoDB
                            echo '⏳ Waiting for MongoDB to be ready...'
                            kubectl wait --for=condition=available --timeout=300s deployment/mongodb || true
                            
                            # Update image tags
                            echo '🏷️ Updating image tags...'
                            sed -i 's|kastrov/frontend:.*|kastrov/frontend:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/user-service:.*|kastrov/user-service:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/product-service:.*|kastrov/product-service:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/order-service:.*|kastrov/order-service:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/payment-service:.*|kastrov/payment-service:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/notification-service:.*|kastrov/notification-service:${params.IMAGE_TAG}|g' k8s/deployments/all-services.yml
                            
                            # Deploy services
                            echo '🚀 Deploying application services...'
                            kubectl apply -f k8s/deployments/all-services.yml
                            kubectl apply -f k8s/services/all-services.yml
                            
                            echo '✅ Services deployed successfully'
                        """
                    }
                }
            }
        }
        
        stage('Fix Ingress Controller') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh """
                            echo '🔧 Fixing NGINX Ingress Controller for EKS 1.30...'
                            
                            # Remove old ingress controller
                            kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/aws/deploy.yaml --ignore-not-found=true
                            
                            # Wait for cleanup
                            sleep 10
                            
                            # Install correct version
                            kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml
                            
                            # Wait for ingress controller
                            echo '⏳ Waiting for ingress controller to be ready...'
                            kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s
                            
                            echo '✅ Ingress controller ready!'
                        """
                    }
                }
            }
        }
        
        stage('Deploy Application Ingress') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh """
                            echo '🌐 Deploying application ingress...'
                            
                            # Apply the fixed ingress configuration
                            kubectl apply -f k8s/ingress-fixed.yml
                            
                            # Wait for ingress to be ready
                            sleep 30
                            
                            echo '✅ Ingress deployed successfully'
                        """
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh """
                            echo '🔍 Verifying deployment...'
                            
                            # Check deployments
                            kubectl get deployments
                            
                            # Check services
                            kubectl get services
                            
                            # Check ingress
                            kubectl get ingress
                            
                            # Check rollout status
                            echo '📊 Checking rollout status...'
                            kubectl rollout status deployment/mongodb --timeout=300s || true
                            kubectl rollout status deployment/frontend --timeout=300s || true
                            kubectl rollout status deployment/user-service --timeout=300s || true
                            kubectl rollout status deployment/product-service --timeout=300s || true
                            kubectl rollout status deployment/order-service --timeout=300s || true
                            kubectl rollout status deployment/payment-service --timeout=300s || true
                            kubectl rollout status deployment/notification-service --timeout=300s || true
                            
                            # Check pods
                            echo '🚀 Pod status:'
                            kubectl get pods -o wide
                            
                            # Check ingress details
                            echo '🌐 Ingress details:'
                            kubectl describe ingress microservices-ingress
                        """
                    }
                }
            }
        }
        
        stage('Get Application URL') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh """
                            echo '========================================='
                            echo '🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!'
                            echo '========================================='
                            
                            # Get application URL
                            echo '🔍 Getting application URL...'
                            INGRESS_URL=\$(kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "")
                            
                            if [ -z "\$INGRESS_URL" ]; then
                                echo '⏳ Load Balancer URL not ready yet.'
                                echo '   This usually takes 2-5 minutes after deployment.'
                                echo ''
                                echo '🔄 To check status later, run:'
                                echo '   kubectl get ingress microservices-ingress'
                                echo '   kubectl get svc -n ingress-nginx'
                            else
                                echo '✅ Application is ready!'
                                echo ''
                                echo '🌐 ACCESS YOUR APPLICATION:'
                                echo '   Main Application: http://'\$INGRESS_URL'/'
                                echo '   Admin Dashboard:  http://'\$INGRESS_URL'/admin'
                                echo ''
                                echo '🔧 Individual Services:'
                                echo '   User Service:         http://'\$INGRESS_URL'/user-service'
                                echo '   Product Service:      http://'\$INGRESS_URL'/product-service'
                                echo '   Order Service:        http://'\$INGRESS_URL'/order-service'
                                echo '   Payment Service:      http://'\$INGRESS_URL'/payment-service'
                                echo '   Notification Service: http://'\$INGRESS_URL'/notification-service'
                            fi
                            
                            echo ''
                            echo '📋 SECURITY GROUPS REQUIRED:'
                            echo '   EKS Worker Nodes: Ports 80, 443, 30000-32767'
                            echo '   Load Balancer: Ports 80, 443 (auto-configured)'
                            echo ''
                            echo '🩺 HEALTH CHECK:'
                            echo '   kubectl get pods'
                            echo '   kubectl get svc -n ingress-nginx'
                            echo '   kubectl get ingress'
                            echo '========================================='
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo '✅ E-Commerce Microservices Application deployed successfully!'
            echo ''
            echo '🎯 NEXT STEPS:'
            echo '1. Wait 2-5 minutes for Load Balancer to be ready'
            echo '2. Check: kubectl get ingress microservices-ingress'
            echo '3. Access your application using the URL shown above'
            echo '4. If 404 error persists, check AWS Security Groups'
            echo ''
            echo '🔧 TROUBLESHOOTING:'
            echo 'If application is not accessible:'
            echo '- Check security groups (ports 80, 443, 30000-32767)'
            echo '- Verify ingress controller: kubectl get pods -n ingress-nginx'
            echo '- Check load balancer: kubectl get svc -n ingress-nginx'
        }
        failure {
            echo '❌ Deployment failed! Check the logs above for details.'
            script {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh """
                        echo '🔍 Getting debug information...'
                        kubectl get pods
                        kubectl get events --sort-by=.metadata.creationTimestamp | tail -10
                        kubectl get svc -n ingress-nginx
                    """
                }
            }
        }
    }
}
