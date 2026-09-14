pipeline {

    agent any

    environment {
        IMAGE_NAME = 'adeelamanat56/myapp'
        IMAGE_TAG  = "${BUILD_NUMBER}"
        
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        

        s

        stage('Build Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE} .
                '''
            }
        }

        

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push ${IMAGE}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose pull
                    docker compose up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 10

                    docker compose ps

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
                docker compose ps || true
                docker compose logs --tail=100 || true
            '''
        }

        
    }
}