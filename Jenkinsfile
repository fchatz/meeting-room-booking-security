pipeline {
    agent any
    stages {
        stage('Environment Check') {
            steps {
                bat 'py -3.14 --version'
                bat 'git --version'
                bat 'if exist reports rmdir /s /q reports'
                bat 'mkdir reports'
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
                bat '.venv\\Scripts\\python.exe -m pytest tests/ -v --junitxml=reports/pytest-results.xml'
            }
        }
        stage('Static Analysis'){
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install bandit==1.9.4'
                bat '.venv\\Scripts\\bandit.exe -r application_api reservation_service scheduling_service packages/scheduling_helper/src -f json -o reports/bandit-results.json --exit-zero'
                bat '.venv\\Scripts\\bandit.exe -r application_api reservation_service scheduling_service packages/scheduling_helper/src -ll'
            }
        }
        stage('Dependency Analysis'){
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install pip-audit==2.10.1'
                bat '.venv\\Scripts\\python.exe -m pip_audit --local --skip-editable'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/pytest-results.xml'
        }
    }
}
