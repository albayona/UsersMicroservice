pipeline {
  agent {
    docker {
      image 'python:3.5.1'
    }

  }
  stages {
    stage('Install Packages') {
      steps {
        sh 'pip3 install -r "requirements.txt"'
      }
    }

    stage('Build') {
      steps {
        echo 'HELLO WORLD'
      }
    }

  }
}