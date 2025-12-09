pipeline {
    agent any
}

environment {
    PYTHONUNBUFFERED = '1'
}

stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('setup Python') {
        steps{
            sh '''
                python3 --version || {echo "python3 missing"; exit 1;}
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                python -m pip --version
            '''
        }
    }

    stage('Install dependencies') {
        steps {
            sh '''
                . .venv/bin/activate
                if [ -f requirements.txt ]; then
                    pip install -r requirements.txt
                else
                    echo "No req.txt file found"
                fi
            '''
        }
    }

    stage('Lint / Basic Checks') {
        steps {
            sh '''
                . .venv/bin/activate
                if command -v flake8 > /dev/null 2>&1; then
                    flake8 || true
                else
                    echo "Flake8 not isntalled" || true
                fi
                python main.py --help || true
            '''
        }
    }

    stage('Run tests') {
        steps {
            sh '''
                . .venv/bin/activate
                if [ -d tests ] || command -v pytest >/dev/null 2>&1; then
                    pytest -q || true
                else
                    echo "No test Found - skipped"
                fi
            '''
        }
    }

    post {
        always {
            sh 'echo "Build finished. Listing workspace:"; ls -la'
            archiveArtifacts artifacts: '**/target/*.jar, **/*.log, requirements.txt', allowEmptyArchive: true
        }
        failure {
           echo "Build failed. Check console log."
        }
    }
}

