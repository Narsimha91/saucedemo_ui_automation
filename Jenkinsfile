pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Workspace') {
            steps {
                bat '''
                    echo ===== Workspace Files =====
                    dir
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    echo ===== Python Version =====
                    python --version

                    echo ===== Creating Virtual Environment =====
                    python -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
    steps {
        bat '''
            venv\\Scripts\\python -m pip install --upgrade pip

            venv\\Scripts\\python -m pip install pytest
            venv\\Scripts\\python -m pip install pytest-xdist
            venv\\Scripts\\python -m pip install pytest-html
            venv\\Scripts\\python -m pip install allure-pytest
            venv\\Scripts\\python -m pip install playwright

            venv\\Scripts\\python -m playwright install
        '''
    }
}
        stage('Run Pytest') {
            steps {
                bat '''
                    echo ===== Running Tests =====

                    venv\\Scripts\\python -m pytest ^
                    -m add_to_cart ^
                    -n 1 ^
                    --buy="1" ^
                    --alluredir=allure-results
                '''
            }
        }
    }

    post {

        always {
            echo '===== Pipeline Finished ====='

            allure([
                includeProperties: false,
                results: [
                    [
                        path: 'allure-results'
                    ]
                ]
            ])
        }

        success {
            echo '===== Tests Passed Successfully ====='
        }

        failure {
            echo '===== Tests Failed ====='
        }
    }
}