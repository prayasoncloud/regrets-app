pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''#!/bin/bash
set -euo pipefail
python3 --version
'''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''#!/bin/bash
set -euo pipefail
pip3 install -r requirements.txt
'''
            }
        }

        stage('Lint / Basic checks') {
            steps {
                sh '''#!/bin/bash
set -euo pipefail
python3 -m py_compile main.py
'''
            }
        }

        stage('Run tests') {
            steps {
                sh '''#!/bin/bash
set -euo pipefail
python3 main.py
'''
            }
        }
    }

    post {
        always {
            sh '''#!/bin/bash
echo "Build finished. Listing workspace:"
ls -la
'''
            archiveArtifacts artifacts: '**/*', allowEmptyArchive: true
        }

        failure {
            echo "Build failed. Check console log."
        }
    }
}
