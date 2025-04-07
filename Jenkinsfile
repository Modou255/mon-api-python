pipeline {
    agent any
    
    environment {
        REPO_URL = 'https://github.com/Modou255/mon-api-python.git'
        ANSIBLE_INVENTORY = 'ansible/inventory.ini'
        ANSIBLE_PLAYBOOK = 'ansible/deploy.yml'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: "${REPO_URL}"
            }
        }
        
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run tests') {
            parallel {
                stage('Unit tests') {
                    steps {
                        sh 'pytest tests/ -v'
                    }
                }
                stage('Coverage') {
                    steps {
                        sh 'pytest --cov=app tests/'
                    }
                }
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                }
                failure {
                    emailext body: 'Les tests ont échoué dans ${BUILD_URL}', 
                    subject: 'Échec des tests - ${JOB_NAME}', 
                    to: 'team@example.com'
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ansible-ssh-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh """
                    export ANSIBLE_HOST_KEY_CHECKING=False
                    ansible-playbook -i ${ANSIBLE_INVENTORY} ${ANSIBLE_PLAYBOOK} \
                    --private-key=${SSH_KEY} \
                    -e repository_url=${REPO_URL}
                    """
                }
            }
        }
    }
    
    post {
        failure {
            slackSend channel: '#devops', 
            color: 'danger', 
            message: "Build ${BUILD_NUMBER} a échoué: ${BUILD_URL}"
        }
        success {
            slackSend channel: '#devops', 
            color: 'good', 
            message: "Build ${BUILD_NUMBER} réussi: ${BUILD_URL}"
        }
    }
}
