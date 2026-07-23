pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\python -m pip install --upgrade pip'
		bat 'call venv\\Scripts\\activate'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {

		bat 'call venv\\Scripts\\activate'
                bat 'pytest -m add_to_cart -n 1 --buy="1" --alluredir=allure-results'
            }
        }
    }

    post {
        success {
            echo 'Pytest passed successfully'
        }

        failure {
            echo 'Tests failed'
        }

        always {
            echo 'Pipeline finished'
        }
    }
}