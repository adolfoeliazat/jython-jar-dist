#!/usr/bin/env bash

# MUST active virtualenv before running script
# workon test6-jython

echo "VirualEnv Jython Jar Fun"
echo $VIRTUAL_ENV

JYTHON_INSTALL="/opt/jython2.7b1"

CUR_DIR="${PWD}"

cd $JYTHON_INSTALL

cp jython.jar blah.jar
zip -r blah.jar Lib
cp blah.jar "$CUR_DIR/."
cd $CUR_DIR
#zip blah.jar __run__.py
