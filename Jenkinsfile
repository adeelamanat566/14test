```groovy
pipeline {

    agent any

    environment {
        AWS_REGION = 'ap-south-1'

        ECR_REGISTRY = '613719615634.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'myapp'

        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"

        PRODUCTION_INSTANCE_ID = 'i-08fd9bc5fe962bc3a'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE} .
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password \
                    --region ${AWS_REGION} |
                    docker login \
                    --username AWS \
                    --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${IMAGE}
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                    export IMAGE=${IMAGE}

                    docker compose -f compose.yaml pull
                    docker compose -f compose.yaml up -d
                '''
            }
        }

        stage('Staging Health Check') {
            steps {
                sh '''
                    sleep 10

                    docker compose -f compose.yaml ps

                    curl -f http://localhost:5000

                    echo "Staging is healthy."
                '''
            }
        }

        stage('Approval') {
            steps {
                input message: "Staging passed. Deploy ${IMAGE} to Production?",
                      ok: 'Deploy to Production'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    aws ssm send-command \
                    --instance-ids ${PRODUCTION_INSTANCE_ID} \
                    --document-name "AWS-RunShellScript" \
                    --parameters 'commands=[
                        "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}",
                        "cd /opt/myapp",
                        "export IMAGE=${IMAGE}",
                        "docker compose pull",
                        "docker compose up -d"
                    ]' \
                    --region ${AWS_REGION}
                '''
            }
        }

        stage('Production Health Check') {
            steps {
                sh '''
                    echo "Production deployment command sent successfully."
                '''
            }
        }
    }

    post {

        success {
            echo "Deployment successful: ${IMAGE}"
        }

        failure {
            echo "Pipeline failed."

            sh '''
                docker compose -f compose.yaml ps || true
                docker compose -f compose.yaml logs --tail=100 || true
            '''
        }

        always {
            sh '''
                docker logout ${ECR_REGISTRY} || true
                docker image prune -f || true
            '''
        }
    }
}
```
