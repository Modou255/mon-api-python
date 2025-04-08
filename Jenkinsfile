pipeline {
    agent any

    environment {
        PYTHON_VIRTUAL_ENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            parallel {
                stage('Unit tests') {
                    steps {
                        script {
                            sh 'pytest --cov=app tests/ --junitxml=results.xml'
                        }
                    }
                }
                stage('Coverage') {
                    steps {
                        script {
                            sh 'pytest --cov=app tests/'
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                // Les étapes de déploiement vont ici
            }
        }
    }

    post {
        always {
            junit '**/results.xml'
            slackSend(channel: '#devops', color: 'danger', message: 'Pipeline échouée', tokenCredentialId: 'slack-api-token')
        }
    }
}
