pipeline {
  agent any

  environment {
    PYTHONUNBUFFERED = '1'
  }

  options {
    timestamps()
    // ansiColor('xterm') // enable if AnsiColor plugin is installed
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        // use a short shell block and ensure any failure stops the stage
        sh '''
          #!/bin/bash
          set -euo pipefail
          python3 --version
          python3 -m venv .venv
          . .venv/bin/activate
          # use the venv pip explicitly to avoid confusion
          .venv/bin/python -m pip install --upgrade pip
          .venv/bin/python -m pip --version
        '''
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          #!/bin/bash
          set -euo pipefail
          . .venv/bin/activate
          if [ -f requirements.txt ]; then
            .venv/bin/pip install -r requirements.txt
          else
            echo "No requirements.txt found"
          fi
        '''
      }
    }

    stage('Lint / Basic checks') {
      steps {
        sh '''
          #!/bin/bash
          set -euo pipefail
          // --- IMPROVEMENT: Removed || true. Build will now fail if linting fails. ---
          . .venv/bin/activate
          if command -v .venv/bin/flake8 >/dev/null 2>&1; then
          echo "Running flake8..."  
            .venv/bin/flake8 // Build fails here if lint errors are found
          else
            echo "flake8 not installed - skipping lint"
          fi

          # run a non-invasive syntax check for the app
           echo "Running python syntax check..."
          .venv/bin/python -m py_compile main.py
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          #!/bin/bash
          set -euo pipefail
          . .venv/bin/activate
          if [ -d tests ] && command -v .venv/bin/pytest >/dev/null 2>&1; then
            echo "Running pytest..."
            .venv/bin/pytest -q
          else
            echo "No tests found or pytest not installed - skipped"
          fi
        '''
      }
    }
  }

  post {
    always {
      sh 'echo "Build finished. Listing workspace:"; ls -la'
      archiveArtifacts artifacts: 'requirements.txt, **/*.log', allowEmptyArchive: true
    }
    failure {
      echo "Build failed. Check console log."
    }
  }
}
