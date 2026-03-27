pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'mkdir -p reports'
                sh 'pytest'
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/*', onlyIfSuccessful: false
            sh 'python scripts/notify_feishu.py'
        }
    }
}

