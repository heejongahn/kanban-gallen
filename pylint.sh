#!/bin/bash

SHPATH=`pwd`
echo pylint --rcfile=${SHPATH}/pylintrc
pylint --rcfile=${SHPATH}/pylintrc $1
