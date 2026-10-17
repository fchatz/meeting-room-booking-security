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
                bat '.venv\\Scripts\\python.exe -m pip install --no-cache-dir -r requirements.txt'
            }
        }
        stage('Initialize Test Database'){
            steps {
                bat 'if exist application_api\\auth.db del /q application_api\\auth.db'
                bat '.venv\\Scripts\\python.exe application_api\\init_auth_db.py'
            }
        }
        stage('Automated Tests'){
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest tests/ -v'
            }
        }
    }
}
