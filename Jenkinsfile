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
                    docker.withTool('MyExplorariServerJenkinsDocker') {
                        docker.build DOCKER_IMAGE
                        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                            docker.image(DOCKER_IMAGE).push()
                        }
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
