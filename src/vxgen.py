import sys
import os
from gen import *
from add import *
from top import *
from tb import *





# Requirement:
	#main entity shoud be by the end of the file
	# entity one line, begin one line
	# use 'end entity'
	# port(


# Problem:
# component port map sequence
# 0 downto 0



		

def pkgGen(arg):
	if len(arg) ==0:
		print('Usage: vxgen pkg <pkg_name> {-a} {-f <folder>}')
		exit(1)
	if '-f' in arg:
		filepath = arg.pop(arg.index('-f') + 1)
		arg.pop(arg.index('-f'))
	else:
		filepath = os.getcwd()
	allfile = os.listdir(filepath)
	filename = arg.pop(0)
	if not filename[-4:] == '.vhd':
		filename = filename + 'vhd'
	fullname = filepath + filename 
	confpath = os.environ["VHDLXGEN_PATH"] + '/conf'
	datapath = os.environ["VHDLXGEN_PATH"] + '/data'
	with open(fullname, 'w+') as file:
		with open(confpath + '/library.conf', 'r') as f:
			for line in f:
				line = line.strip()
				if line[0] != '#':
					file.write( line+ '\n')
		file.write('\n')
		with open(datapath + '/pkg.vd', 'r') as f:
			for line in f:
				line = line.replace('$pkg_name', filename[:-4])
				file.write( line)
	
	if '-a' in arg:
		for file in allfile:
			with open(filepath + file, 'a') as f:
				f.seek(0, 0)
				f.write('library work;\nuse work.'+filename[:-4]+'.all;\n')
	

def printInfo():
	print('\nVHDL-Xgen  Version: 0.0\n');
	
	
	

def main():
	if len(sys.argv) < 2:
		print("Usage: python vxgen.py <func> <args>")
		exit(1)
	if  not "VHDLXGEN_PATH" in os.environ:
		print("Please set environment before use.\n")
		exit(1)
	Fun =  sys.argv[1]
	if Fun == 'gen':
		generation(sys.argv[2:])
	elif Fun == 'add':
		addComponents(sys.argv[2:])
	elif Fun == 'top':
		topGen(sys.argv[2:])
	elif Fun == 'tb':
		tbGen(sys.argv[2:])
	elif Fun == 'pkg':
		pgkGen(sys.argv[2:])
	elif Fun == 'version':
		printInfo()
	else :
		print("Usage: python vxgen.py <func> <args>")
		exit(1)


if __name__ == '__main__':
    main()

