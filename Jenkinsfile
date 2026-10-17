pipeline {
    agent any

    stages {
        stage('Environment Check') {
            steps {
                bat 'py -3.14 --version'
                bat 'git --version'
            }
        }
    }
}
