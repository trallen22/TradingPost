pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('test') {
            steps {
                sh 'echo all tests passed'
            }
        }
        stage('deploy') {
            steps {
                sh 'echo app was deployed'
            }
        }
    }
}