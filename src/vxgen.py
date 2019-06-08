import sys
import os
import glob
#import os.path.join as join
from gen import generation
from add import *
from top import *
from tb import *








# Problem:
# 
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
	cufolder = filepath.split(os.sep)[-1]
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
	fullname = os.path.join(filepath , filename)
	writeFrame(fullname)
	datapath = os.path.join(os.environ["VHDLXGEN_PATH"] , 'data')
	with open(fullname, 'a') as file:
		with open(os.path.join(datapath , 'pkg.vd'), 'r') as f:
			for line in f:
				line = line.replace('$pkg_name', filename[:-4])
				file.write( line)
	
	if '-a' in arg:
		for file in allfile:
			with open(os.path.join(filepath , file), 'r') as f:
				dataf = f.readlines()
			pt = findEntityHead(dataf)
			dataf.insert(pt,'library work;\nuse work.'+filename[:-4]+'.all;\n')
			with open(os.path.join(filepath ,file), 'w') as f:
				for line in dataf:
					f.write(line)
	

def printInfo():
	datapath = os.path.join(os.environ["VHDLXGEN_PATH"] , 'data')
	with open(os.path.join(datapath , 'version.vd'), 'r') as file:
		for line in file:
			sys.stdout.write(line)
	
def printHelp():	
	datapath = os.path.join(os.environ["VHDLXGEN_PATH"] , 'data')
	with open(os.path.join(datapath , 'help.vd'), 'r') as file:
		for line in file:
			sys.stdout.write(line)
	

def main(arg):
	if len(arg) == 0:
		print("Usage: vxgen <fun> <arg>, command \'vxgen help\' for more info.")
		exit(1)
	if  not "VHDLXGEN_PATH" in os.environ:
		print("Please set environment before use.\n")
		exit(1)
	Fun =  arg[0]
	if Fun == 'gen':
		generation(arg[1:])
	elif Fun == 'add':
		addComponents(arg[1:])
	elif Fun == 'top':
		topGen(arg[1:])
	elif Fun == 'tb':
		tbGen(arg[1:])
	elif Fun == 'pkg':
		pkgGen(arg[1:])
	elif Fun == 'version':
		printInfo()
	elif Fun == 'help':
		printHelp()
	else :
		print("Usage: vxgen <fun> <arg>, command \'vxgen help\' for more info.")
		exit(1)

def existonevsh():
	filenum = 0
	for file in os.listdir('.'):
		if 'vsh' in file:
			filenum += 1
	if filenum == 1:
		return True
	elif filenum == 0:
		return False
	else:
		print('ERROR: More than one vsh file found in current folder. Omit both.')
		return False

def genFromScript(vshpath):
	if vshpath == '.':
		if len(glob.glob('*.vsh')) == 0:
			print('Can\'t find vsh file in current folder. \nFor usage: command \'vxgen help\'')
			exit(1)
		with open(glob.glob('*.vsh')[0], 'r') as vsh:
			data = vsh.readlines()
	else:
		with open(vshpath, 'r') as vsh:
			data = vsh.readlines()
	for line in data:
		if line.strip() != '':
			print('>>> '+line)
			arg = []
			arg = arg + line.split()
			if '' in arg:
				arg.pop(arg.index(''))
			for i in arg:
				arg[arg.index(i)] = i.strip()
			main(arg)
	print('>>> Done')


if __name__ == '__main__':
	arg = sys.argv[1:]
	if len(arg) == 1 and '.vsh' in arg[0]:
		genFromScript(arg[0])
	elif len(arg) ==0 and existonevsh():
		genFromScript('.')
	else:
		main(arg)

