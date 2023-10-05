pipeline {
    agent any

    stages {
        stage('Echo Message') {
            steps {
                echo 'Hello, Jenkins! This is a simple Jenkins pipeline.'
            }
        }
    }

    post {
        success {
            echo 'The pipeline ran successfully!'
        }
        failure {
            echo 'The pipeline failed.'
        }
    }
}