# Jenkins Setup Guide for E-Commerce Microservices

## Prerequisites Setup

### 1. Jenkins Configuration
Ensure Jenkins is running on port 8080 with the following configurations:

#### Required Plugins
Install these plugins in Jenkins:
- Docker Pipeline
- Kubernetes CLI
- AWS Steps
- Pipeline: Stage View
- Blue Ocean (optional, for better UI)

#### Credentials Configuration
Configure these credentials in Jenkins (Manage Jenkins → Credentials):

1. **DockerHub Credentials** (ID: `dockerhub-creds`)
   - Type: Username with password
   - Username: `kastrov`
   - Password: Your DockerHub password

2. **AWS Credentials** (ID: `aws-creds`)
   - Type: AWS Credentials
   - Access Key ID: Your AWS Access Key
   - Secret Access Key: Your AWS Secret Key

#### Tool Configuration
Configure Docker tool (Manage Jenkins → Global Tool Configuration):
- Name: `docker`
- Install automatically: ✓
- Add Docker installer

### 2. EKS Cluster Setup
Ensure your EKS cluster `kastro-eks` is running in `us-east-1`:

```bash
# Verify cluster
aws eks describe-cluster --name kastro-eks --region us-east-1

# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name kastro-eks
```

### 3. NGINX Ingress Controller
Install NGINX Ingress Controller in your EKS cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml
```

## Jenkins Job Setup

### Option 1: Main Deployment Pipeline (Recommended)

1. **Create New Pipeline Job**
   - Job name: `ecommerce-microservices-deployment`
   - Type: Pipeline

2. **Configure Pipeline**
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/KastroVKiran/ecom-app-new-kastro.git`
   - Branch: `master`
   - Script Path: `Jenkinsfile`

3. **Build Parameters**
   The pipeline includes these parameters:
   - `IMAGE_TAG`: Docker image tag (default: latest)
   - `DEPLOY_ENV`: Environment (dev/staging/prod)
   - `DEPLOY_TYPE`: Service to deploy (all/individual services)

### Option 2: Individual Service Pipelines

Create separate pipeline jobs for each service:

1. **user-service-pipeline**
   - Script Path: `user-service/Jenkinsfile`

2. **product-service-pipeline**
   - Script Path: `product-service/Jenkinsfile`

3. **order-service-pipeline**
   - Script Path: `order-service/Jenkinsfile`

4. **payment-service-pipeline**
   - Script Path: `payment-service/Jenkinsfile`

5. **notification-service-pipeline**
   - Script Path: `notification-service/Jenkinsfile`

6. **frontend-pipeline**
   - Script Path: `frontend/Jenkinsfile`

## Deployment Process

### 1. First Time Deployment

1. **Run Main Pipeline**
   ```
   Job: ecommerce-microservices-deployment
   Parameters:
   - IMAGE_TAG: v1.0
   - DEPLOY_ENV: dev
   - DEPLOY_TYPE: all
   ```

2. **Monitor Deployment**
   - Check Jenkins console output
   - Verify Kubernetes resources
   - Get application URL from pipeline output

### 2. Individual Service Updates

For updating individual services:
```
Parameters:
- IMAGE_TAG: v1.1
- DEPLOY_ENV: dev
- DEPLOY_TYPE: user-service (or specific service)
```

### 3. Production Deployment

```
Parameters:
- IMAGE_TAG: v1.0-prod
- DEPLOY_ENV: prod
- DEPLOY_TYPE: all
```

## Verification Commands

After deployment, verify using these commands:

```bash
# Check cluster connection
kubectl get nodes

# Check deployments
kubectl get deployments

# Check services
kubectl get services

# Check ingress
kubectl get ingress

# Check pods
kubectl get pods -o wide

# Get application URL
kubectl get ingress microservices-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Check logs
kubectl logs -l app=frontend
kubectl logs -l app=user-service
```

## Troubleshooting

### Common Issues

1. **Docker Build Fails**
   - Check Dockerfile syntax
   - Verify base image availability
   - Check file permissions

2. **Kubernetes Deployment Fails**
   - Verify EKS cluster connectivity
   - Check AWS credentials
   - Verify image exists in DockerHub

3. **Ingress Not Working**
   - Check NGINX Ingress Controller status
   - Verify ingress configuration
   - Check security groups and load balancer

4. **MongoDB Connection Issues**
   - Check MongoDB pod status
   - Verify service connectivity
   - Check environment variables

### Debug Commands

```bash
# Check pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>

# Check ingress controller
kubectl get pods -n ingress-nginx

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Port forward for testing
kubectl port-forward service/frontend 8080:3000
```

## Monitoring and Maintenance

### Regular Checks
- Monitor pod health: `kubectl get pods`
- Check resource usage: `kubectl top pods`
- Review logs: `kubectl logs -f <pod-name>`
- Verify ingress: `kubectl describe ingress`

### Scaling
```bash
# Scale services
kubectl scale deployment frontend --replicas=3
kubectl scale deployment user-service --replicas=2
```

### Updates
- Use Jenkins pipeline with new IMAGE_TAG
- Monitor rollout: `kubectl rollout status deployment/<service-name>`
- Rollback if needed: `kubectl rollout undo deployment/<service-name>`

## Security Best Practices

1. **Secrets Management**
   - Store sensitive data in Kubernetes secrets
   - Use AWS IAM roles for service accounts
   - Rotate credentials regularly

2. **Network Security**
   - Configure network policies
   - Use TLS for ingress
   - Restrict service communication

3. **Image Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Keep images updated

## Backup and Recovery

### MongoDB Backup
```bash
# Create backup
kubectl exec -it <mongodb-pod> -- mongodump --out /backup

# Copy backup
kubectl cp <mongodb-pod>:/backup ./mongodb-backup

# Restore backup
kubectl cp ./mongodb-backup <mongodb-pod>:/restore
kubectl exec -it <mongodb-pod> -- mongorestore /restore
```

This setup provides a complete CI/CD pipeline for your microservices application with proper monitoring, scaling, and maintenance procedures.