#!/usr/bin/env bash

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
    export BLDR_BUILD=$HOME/work/build
    mkdir -p $BLDR_BUILD
}


report_config() {
    printenv | sort | grep "BLDR_*"
    
    python3 --version
    alias
}

create_home_environment
report_config