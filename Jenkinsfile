pipeline {
  agent {
    label "jenkins-python"
  }
  environment {
    ORG = 'raufer'
    APP_NAME = 'telecom-churn'
    DOCKER_REGISTRY_ORG = 'telecom-churn'
    CHARTMUSEUM_CREDS = credentials('jenkins-x-chartmuseum')
    //AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
    //AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
  }
  stages {
    stage('CI Build and push snapshot') {
      when {
        branch 'PR-*'
      }
      environment {
        PREVIEW_VERSION = "0.0.0-SNAPSHOT-$BRANCH_NAME-$BUILD_NUMBER"
        PREVIEW_NAMESPACE = "$APP_NAME-$BRANCH_NAME".toLowerCase()
        HELM_RELEASE = "$PREVIEW_NAMESPACE".toLowerCase()
      }
      steps {
        container('python') {
          sh "python -m unittest"
          sh "export VERSION=$PREVIEW_VERSION && skaffold build -f skaffold.yaml"
          sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:$PREVIEW_VERSION"
          dir('./charts/preview') {
            sh "make preview"
            sh "jx preview --app $APP_NAME --dir ../.."
          }
        }
      }
    }
    stage('Build') {
      when {
        branch 'master'
      }
      steps {
        container('python') {
          // ensure we're not on a detached head
          sh "git checkout master"
          sh "git config --global credential.helper store"
          sh "jx step git credentials"

          // so we can retrieve the version in later steps
          sh "echo \$(jx-release-version) > VERSION"
          sh "jx step tag --version \$(cat VERSION)"

	      sh '''
	      export VERSION=`(cat VERSION)`
	      for file in pipeline/*/ ; do
	        if [[ -d "$file" && ! -L "$file" ]]; then
	          echo "Building $file";
	          cd $file;
	          STEP=$(basename $file)
	          IMAGE=$DOCKER_REGISTRY/$DOCKER_REGISTRY_ORG/$STEP:$VERSION
	          echo $IMAGkE
	          docker build --network=host -t $IMAGE . ;
	          docker push $IMAGE;
	          cd ../..;
	        fi;
	      done
	      '''

	      sh '''
	      export VERSION=`(cat VERSION)` && \
	      export IMAGE=$DOCKER_REGISTRY/$DOCKER_REGISTRY_ORG/inference:$VERSION && \
	      cd inference && \
	      docker build --network=host -t $IMAGE . && \
	      docker push $IMAGE && \
	      cd ../
	      '''

	      //sh "jx step post build --image $DOCKER_REGISTRY/$ORG/$APP_NAME:\$(cat VERSION)"

 	      // Compile Kubeflow Pipeline
	      sh "curl https://bootstrap.pypa.io/get-pip.py | python3"
          sh "pip3 install -r pipeline/requirements.txt"
	      sh "export VERSION=`(cat VERSION)` && python3 pipeline/pipeline.py"
        }
      }
    }
    stage('Test') {
      when {
        branch 'master'
      }
      steps {
        container('python') {
          sh "for file in pipeline/*/ ; do python -m unittest; done"
        }
      }
    }
    stage('Release') {
      when {
        branch 'master'
      }
      steps {
        container('python') {
	    sh "kubectl port-forward -n seldon service/ambassador 8080:80 &"
	    sh "export VERSION=`(cat VERSION)` && python3 pipeline/post_run.py"
        }
      }
    }
    stage('Promote to Environments') {
      when {
        branch 'master'
      }
      steps {
        container('python') {
          dir('./charts/telecom-churn') {
            sh "jx step changelog --version v\$(cat ../../VERSION)"

            // Add the correct IMAGE:VERSION value in values.yaml
            sh '''
            export VERSION=`(cat ../../VERSION)` && \
            export IMAGE=$DOCKER_REGISTRY/$DOCKER_REGISTRY_ORG/inference:$VERSION && \
            python3 ../overwrite.py values.yaml model.image.name $IMAGE
            '''

            sh 'cat values.yaml'

            // release the helm chart
            sh "jx step helm release"

            // promote through all 'Auto' promotion Environments
            sh "jx promote -b --all-auto --timeout 1h --version \$(cat ../../VERSION)"
          }
        }
      }
    }
  }
  post {	
        always {	
          cleanWs()	
        }	
  }
}
