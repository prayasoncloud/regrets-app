pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        VENV_DIR = '.venv'
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
#!/bin/bash
set -euo pipefail

echo "Python version:"
python3 --version

echo "Creating virtual environment..."
python3 -m venv ${VENV_DIR}

echo "Upgrading pip..."
${VENV_DIR}/bin/python -m pip install --upgrade pip
${VENV_DIR}/bin/pip --version
'''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
#!/bin/bash
set -euo pipefail

if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    ${VENV_DIR}/bin/pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping."
fi
'''
            }
        }

        stage('Lint / Basic checks') {
            steps {
                sh '''
#!/bin/bash
set -euo pipefail

if command -v ${VENV_DIR}/bin/flake8 >/dev/null 2>&1; then
    echo "Running flake8..."
    ${VENV_DIR}/bin/flake8 .
else
    echo "flake8 not installed, skipping lint."
fi

echo "Running Python syntax check..."
${VENV_DIR}/bin/python -m py_compile main.py
'''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
#!/bin/bash
set -euo pipefail

if [ -d tests ] && command -v ${VENV_DIR}/bin/pytest >/dev/null 2>&1; then
    echo "Running pytest..."
    ${VENV_DIR}/bin/pytest -q
else
    echo "No tests found or pytest not installed, skipping."
fi
'''
            }
        }
    }

    post {
        always {
            sh '''
echo "Build finished. Listing workspace:"
ls -la
'''
            archiveArtifacts artifacts: 'requirements.txt, **/*.log', allowEmptyArchive: true
        }
        failure {
            echo "Build failed. Check console log."
        }
    }
}
