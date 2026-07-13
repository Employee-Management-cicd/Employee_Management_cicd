pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "priyal9497/employee-app"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Cloning repository from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running automated tests with pytest...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
                bat "docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_IMAGE%:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '⬆️ Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds-teammate',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                bat '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout restart deployment/emp-cicd-app
                    kubectl rollout status deployment/emp-cicd-app --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline PASSED! New version deployed to Kubernetes.'
        }
        failure {
            echo '💥 Pipeline FAILED! Check the red stage above.'
        }
        always {
            bat 'docker logout || exit 0'
        }
    }
}