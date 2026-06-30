pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t employee-management .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker rm -f employee-management-container || exit 0'
                bat 'docker run -d --name employee-management-container -p 5000:5000 employee-management'
            }
        }

    }
}