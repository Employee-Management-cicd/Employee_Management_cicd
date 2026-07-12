pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sneha0206/employee-app"
        DOCKER_TAG   = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip3 install --break-system-packages -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests with pytest...'
                sh 'python3 -m pytest tests/ -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh 'docker rm -f employee-management-container || true'
                sh "docker run -d --name employee-management-container -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo '✅ Application deployed! Visit localhost:5000'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline PASSED! New version is live.'
        }
        failure {
            echo '💥 Pipeline FAILED! Check the stage that went red.'
        }
    }
}
