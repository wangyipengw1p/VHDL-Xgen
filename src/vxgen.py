import sys
import os
from gen import *
from add import *
from top import *
from tb import *





# Requirement:
	#main entity shoud be by the end of the file
	# use 'end entity'


# Problem:
# component port map sequence
# 0 downto 0


def is_not_pkg(name):
	if name[-4:] == '.vhd' and not 'pkg' in name:
		return True
	else:
		return False
		

def pkgGen(arg):
	
	
	if '-f' in arg:
		filepath = arg.pop(arg.index('-f') + 1)
		arg.pop(arg.index('-f'))
	else:
		filepath = os.getcwd()

	allfile = os.listdir(filepath)
	allfile = filter(is_not_pkg,allfile)
	cufolder = filepath.split('/')[-1]
	if len(arg) == 0:
		print('Info: package name not specified. Use ' + cufolder + '_pkg :)\n')
		filename = cufolder + '_pkg'
	elif '-' in arg[0]:
		print('Info: package name not specified. Use ' + cufolder + '_pkg :)\n')
		filename = cufolder + '_pkg'
	else:
		filename = arg.pop(0)
	if not filename[-4:] == '.vhd':
		filename = filename + '.vhd'
	fullname = filepath + '/' + filename 
	writeFrame(fullname)
	datapath = os.environ["VHDLXGEN_PATH"] + '/data'
	with open(fullname, 'a') as file:
		with open(datapath + '/pkg.vd', 'r') as f:
			for line in f:
				line = line.replace('$pkg_name', filename[:-4])
				file.write( line)
	
	if '-a' in arg:
		for file in allfile:
			with open(filepath + '/' + file, 'r') as f:
				dataf = f.readlines()
			pt = findEntityHead(dataf)
			dataf.insert(pt,'library work;\nuse work.'+filename[:-4]+'.all;\n')
			with open(filepath + '/' + file, 'w') as f:
				for line in dataf:
					f.write(line)
	

def printInfo():
	datapath = os.environ["VHDLXGEN_PATH"] + '/data'
	with open(datapath + '/version.vd', 'r') as file:
		for line in file:
			print(line)
	
def printHelp():	
	datapath = os.environ["VHDLXGEN_PATH"] + '/data'
	with open(datapath + '/help.vd', 'r') as file:
		for line in file:
			print(line)
	

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
		pkgGen(sys.argv[2:])
	elif Fun == 'version':
		printInfo()
	elif Fun == 'help':
		printHelp()
	else :
		print("Usage: python vxgen.py <func> <args>")
		exit(1)


if __name__ == '__main__':
    main()

