pipeline {
    agent any

    stages {
        stage('Environment Check') {
            steps {
                bat 'py -3.14 --version'
                bat 'git --version'
            }
        }
        stage('Install Dependencies'){
            steps {
                bat 'py -3.14 -m venv --clear .venv'
                bat '.\\.venv\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }
    }
}
