#!/bin/sh
basepath=$(cd `dirname $0`; pwd) #get cwd
echo  >> ~/.bashrc
# You can also custom the following by yourself
echo 'export VHDLXGEN_PATH='$basepath >> ~/.bashrc           # set the environment variable necessary for this tool
echo alias vxgen=\'python $basepath/src/vxgen.py\'  >> ~/.bashrc         # set alias
