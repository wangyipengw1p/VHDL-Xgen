basepath=$(cd `dirname $0`; pwd) #get cwd
echo  >> ~/.bashrc
echo 'export VHDLXGEN_PATH='$basepath >> ~/.bashrc
echo alias vxgen='python '$basepath'/src/vxgen.py'  >> ~/.bashrc
