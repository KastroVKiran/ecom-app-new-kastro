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
        
        stage('Build and Push Docker Images') {
            parallel {
                stage('Frontend') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'frontend'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def frontendImage = docker.build("${DOCKERHUB_USERNAME}/frontend:${params.IMAGE_TAG}", "./frontend")
                                frontendImage.push()
                                frontendImage.push("latest")
                            }
                        }
                    }
                }
                
                stage('User Service') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'user-service'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def userImage = docker.build("${DOCKERHUB_USERNAME}/user-service:${params.IMAGE_TAG}", "./user-service")
                                userImage.push()
                                userImage.push("latest")
                            }
                        }
                    }
                }
                
                stage('Product Service') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'product-service'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def productImage = docker.build("${DOCKERHUB_USERNAME}/product-service:${params.IMAGE_TAG}", "./product-service")
                                productImage.push()
                                productImage.push("latest")
                            }
                        }
                    }
                }
                
                stage('Order Service') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'order-service'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def orderImage = docker.build("${DOCKERHUB_USERNAME}/order-service:${params.IMAGE_TAG}", "./order-service")
                                orderImage.push()
                                orderImage.push("latest")
                            }
                        }
                    }
                }
                
                stage('Payment Service') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'payment-service'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def paymentImage = docker.build("${DOCKERHUB_USERNAME}/payment-service:${params.IMAGE_TAG}", "./payment-service")
                                paymentImage.push()
                                paymentImage.push("latest")
                            }
                        }
                    }
                }
                
                stage('Notification Service') {
                    when {
                        anyOf {
                            params.DEPLOY_TYPE == 'all'
                            params.DEPLOY_TYPE == 'notification-service'
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                                def notificationImage = docker.build("${DOCKERHUB_USERNAME}/notification-service:${params.IMAGE_TAG}", "./notification-service")
                                notificationImage.push()
                                notificationImage.push("latest")
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
                            echo 'Configuring kubectl for EKS cluster...'
                            aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER_NAME}
                            
                            echo 'Verifying cluster connection...'
                            kubectl get nodes
                            
                            echo 'Deploying MongoDB...'
                            kubectl apply -f k8s/mongodb/
                            
                            echo 'Waiting for MongoDB to be ready...'
                            kubectl wait --for=condition=available --timeout=300s deployment/mongodb
                            
                            echo 'Updating image tags in deployment files...'
                            sed -i 's|kastrov/frontend:.*|kastrov/frontend:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/user-service:.*|kastrov/user-service:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/product-service:.*|kastrov/product-service:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/order-service:.*|kastrov/order-service:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/payment-service:.*|kastrov/payment-service:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            sed -i 's|kastrov/notification-service:.*|kastrov/notification-service:${params.IMAGE_TAG}|g\' k8s/deployments/all-services.yml
                            
                            echo 'Deploying all services...'
                            kubectl apply -f k8s/deployments/all-services.yml
                            kubectl apply -f k8s/services/all-services.yml
                            
                            echo 'Deploying ingress controller...'
                            kubectl apply -f k8s/ingress.yml
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
                            echo 'Verifying deployments...'
                            kubectl get deployments
                            kubectl get services
                            kubectl get ingress
                            
                            echo 'Checking rollout status...'
                            kubectl rollout status deployment/mongodb --timeout=300s
                            kubectl rollout status deployment/frontend --timeout=300s
                            kubectl rollout status deployment/user-service --timeout=300s
                            kubectl rollout status deployment/product-service --timeout=300s
                            kubectl rollout status deployment/order-service --timeout=300s
                            kubectl rollout status deployment/payment-service --timeout=300s
                            kubectl rollout status deployment/notification-service --timeout=300s
                            
                            echo 'Getting pod status...'
                            kubectl get pods -o wide
                            
                            echo 'Getting ingress details...'
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
                            echo 'DEPLOYMENT COMPLETED SUCCESSFULLY!'
                            echo '========================================='
                            echo 'Getting application URL...'
                            
                            INGRESS_URL=\$(kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
                            
                            if [ -z "\$INGRESS_URL" ]; then
                                echo 'Ingress URL not ready yet. Please check after a few minutes:'
                                echo 'kubectl get ingress microservices-ingress'
                            else
                                echo 'Application is available at: http://\$INGRESS_URL'
                                echo 'Admin Dashboard: http://\$INGRESS_URL/admin'
                            fi
                            
                            echo '========================================='
                            echo 'Service URLs (internal):'
                            echo 'Frontend: http://\$INGRESS_URL/'
                            echo 'User Service: http://\$INGRESS_URL/user-service'
                            echo 'Product Service: http://\$INGRESS_URL/product-service'
                            echo 'Order Service: http://\$INGRESS_URL/order-service'
                            echo 'Payment Service: http://\$INGRESS_URL/payment-service'
                            echo 'Notification Service: http://\$INGRESS_URL/notification-service'
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
            echo 'Check the console output above for the application URL.'
        }
        failure {
            echo '❌ Deployment failed! Check the logs above for details.'
            script {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh """
                        echo 'Deployment failed. Getting debug information...'
                        kubectl get pods
                        kubectl get events --sort-by=.metadata.creationTimestamp
                    """
                }
            }
        }
    }
}