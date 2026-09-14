pipeline {

    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '613719615634.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'myapp'

        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
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

        stage('Deploy') {
            steps {
                sh '''
                    export IMAGE=${IMAGE}

                    docker compose -f compose.yaml pull
                    docker compose -f compose.yaml up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 10

                    docker compose -f compose.yaml ps

                    curl -f http://localhost:5000

                    echo "Application is healthy."
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
