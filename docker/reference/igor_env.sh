#!/usr/bin/env bash

check_aws_creds_exist() {
    echo "Confirming that AWS credentials have been set"
    if [[ -z AWS_ACCESS_KEY_ID ]]; then
        echo "AWS_ACCESS_KEY_ID not set"
        exit -1
    fi
    if [[ -z AWS_SECRET_ACCESS_KEY ]]; then
        echo "AWS_SECRET_ACCESS_KEY not set"
        exit -1
    fi
    mkdir -p $HOME/.aws
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile default
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile default
    if [[ -v AWS_SESSION_TOKEN ]]; then
        aws configure set aws_session_token $AWS_SESSION_TOKEN --profile default
    fi
    if [[ -v AWS_EXTERNAL_PROVIDED ]]; then
        aws configure set aws_access_key_id $AWS_EXTERNAL_ACCESS_KEY_ID --profile external
        aws configure set aws_secret_access_key $AWS_EXTERNAL_SECRET_ACCESS_KEY --profile external
        if [[ -v AWS_EXTERNAL_SESSION_TOKEN ]]; then
            aws configure set aws_session_token $AWS_EXTERNAL_SESSION_TOKEN --profile external
        fi
    fi
    # echo
    # cat $HOME/.aws/credentials
    # echo
}

create_home_environment() {
    echo "Setting up the $HOME environment"
    #ls -R
    # Set things up to allow the use of JFrog virtual PyPi repo
    mkdir -p $HOME/.pip
    # Fix things up for a local pip configuration
    # to avoid warnings for non-root installs in the container
    mkdir -p $HOME/.local
    mkdir -p $HOME/.local/bin
    export PATH=$HOME/.local/bin:$PATH:/usr/local/go/bin
    # Set up structure for out-of-tree builds
    export IGOR_BUILD=$HOME/work/build
    mkdir -p $IGOR_BUILD
    # Create an alias for nuget
    # alias nuget="mono /usr/local/bin/nuget.exe"
}

create_codeartifact_environment() {
    # Import a default codeartifacts configuration
    echo "Confirming that AWS CodeArtifact configs have been set"
    mkdir -p $HOME/.aws
    CAAR=$HOME/.aws/codeartifacts
    echo "[default]" > $CAAR
    echo "aws_codeartifact_repo = ${AWS_REPO}" >> $CAAR
    echo "aws_codeartifact_domain = ${AWS_DOMAIN}" >> $CAAR
    echo "aws_codeartifact_domain_owner = ${AWS_DOMOWN}" >> $CAAR
    echo "aws_codeartifact_region = ${AWS_REGION}" >> $CAAR
    echo "aws_codeartifact_profile = default" >> $CAAR

    if [[ -v AWS_EXTERNAL_PROVIDED ]]; then
        echo "[external]" >> $CAAR
        echo "aws_codeartifact_repo = ${AWS_EXTERNAL_REPO}" >> $CAAR
        echo "aws_codeartifact_domain = ${AWS_EXTERNAL_DOMAIN}" >> $CAAR
        echo "aws_codeartifact_domain_owner = ${AWS_EXTERNAL_DOMOWN}" >> $CAAR
        echo "aws_codeartifact_region = ${AWS_EXTERNAL_REGION}" >> $CAAR
        echo "aws_codeartifact_profile = external" >> $CAAR
    fi

    # echo
    # cat $CAAR
    # echo

    # Setup pip to use the CodeArtifact repo that will supply igor and other Python packages
    mkdir -p $HOME/.pip
    if [[ -v AWS_EXTERNAL_PROVIDED ]]; then
        echo "aws codeartifact login --tool pip --repository ${AWS_EXTERNAL_REPO} --domain ${AWS_EXTERNAL_DOMAIN}  --domain-owner ${AWS_EXTERNAL_DOMOWN} --region ${AWS_EXTERNAL_REGION} --profile external"
        aws codeartifact login --tool pip --repository ${AWS_EXTERNAL_REPO} --domain ${AWS_EXTERNAL_DOMAIN}  --domain-owner ${AWS_EXTERNAL_DOMOWN}  --region ${AWS_EXTERNAL_REGION} --profile external
        echo "aws codeartifact login --tool twine --repository ${AWS_EXTERNAL_REPO} --domain ${AWS_EXTERNAL_DOMAIN}  --domain-owner ${AWS_EXTERNAL_DOMOWN}  --region ${AWS_EXTERNAL_REGION} --profile external"
        aws codeartifact login --tool twine --repository ${AWS_EXTERNAL_REPO} --domain ${AWS_EXTERNAL_DOMAIN}  --domain-owner ${AWS_EXTERNAL_DOMOWN}  --region ${AWS_EXTERNAL_REGION} --profile external
        
        export IGOR_PACKAGE_REPOSITORY=external
    else
        echo "aws codeartifact login --tool pip --repository ${AWS_REPO} --domain ${AWS_DOMAIN}  --domain-owner ${AWS_DOMOWN}  --region ${AWS_REGION} --profile default"
        aws codeartifact login --tool pip --repository ${AWS_REPO} --domain ${AWS_DOMAIN}  --domain-owner ${AWS_DOMOWN}  --region ${AWS_REGION} --profile default
        echo "aws codeartifact login --tool twine --repository ${AWS_REPO} --domain ${AWS_DOMAIN}  --domain-owner ${AWS_DOMOWN}  --region ${AWS_REGION} --profile default"
        aws codeartifact login --tool twine --repository ${AWS_REPO} --domain ${AWS_DOMAIN}  --domain-owner ${AWS_DOMOWN}  --region ${AWS_REGION} --profile default

        export IGOR_PACKAGE_REPOSITORY=default
    fi
}


report_config() {
    # printenv | sort | grep "AWS_*"
    printenv | sort | grep "IGOR_*"
    
    python3 --version
    alias
}

create_home_environment
check_aws_creds_exist
create_codeartifact_environment
report_config