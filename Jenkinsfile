pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('DockerHubAC')
        DOCKER_IMAGE = 'kutaykaracair/explorari-server:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git url: 'https://github.com/ahmetkutay/explorariServer.git'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.build DOCKER_IMAGE
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Image push successful!'
        }
        failure {
            echo 'Image push failed!'
        }
    }
}
