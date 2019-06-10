import sys
import os
#import os.path.join as join
from gen import *
from add import *

# Functions:
	# is_component(a)
	# topGen(arg)



def is_component(a):
	if a[-4:] == '.vhd' and (not 'tb' in a) and(not 'TOP' in a) and (not 'pkg' in a):
		return True
	else:
		return False


def topGen(arg):
	
	if '-f' in arg:
		filepath = arg.pop(arg.index('-f') + 1)
		arg.pop(arg.index('-f'))
	else:
		filepath = os.getcwd()
	allfile = os.listdir(filepath)
	if '-n' in arg:
		arg.pop(arg.index('-n'))
		auto = False
	else:
		auto = True

	if len(arg) == 0 :
		filename = os.path.join(filepath , filepath.split(os.sep)[-1] + '_TOP.vhd')
		topname = filepath.split(os.sep)[-1] + '_TOP'
		print('Info: filename not specified, use ' + topname + '.vhd\n')
		print('Info: No ports specified in top file.\n')
	elif '-' in arg[0]:
		filename = os.path.join(filepath , filepath.split(os.sep)[-1] + '_TOP.vhd')
		topname = filepath.split(os.sep)[-1] + '_TOP'
		print('Info: filename no specified, use ' + topname + '.vhd\n')
	else:
		filename = arg.pop(0)
		if not len(filename.split(os.sep)) == 1:
			print('Warning: <filename> should not contain path. Use -f <folder> to change.\nWarning: <folder> using default: '+os.getcwd()+'\n')
		if not  filename[-4:] == '.vhd':
			topname = filename
			filename = os.path.join(filepath , filename + '.vhd')
		else:
			topname = filename[:-4]
			filename = os.path.join(filepath , filename)
	allfile = filter(is_component, allfile)

	if len(arg) == 0:
		writeFrame(filename)
		writeEntity(filename, topname)
		for item in allfile:
			addcomponent(filename,os.path.join(filepath,item), auto)
	else:
		if '-u' in arg and '-c' in arg:
			print('Can\'t specify -c and -u at the same time.')
			exit(1)
		if '-c' in arg:
			allfile1 = []
			argindex = arg.index('-c')
			arg.pop(argindex)
			while len(arg) != 0 and (argindex < len(arg)) and (not '-' in arg[argindex]):
				if not arg[argindex][-4:] == '.vhd':
					arg[argindex] = arg[argindex] + '.vhd'
				if not arg[argindex] in allfile:
					print('ERROR: component' +  arg[argindex] + ' not found in ' + filepath+'.\n')
					exit(1)
				allfile1.append(arg[argindex])
				arg.pop(argindex)
			writeFrame(filename)
			writeEntity(filename, topname)
			addports(filename, arg)
			for item in allfile1:
				addcomponent(filename,os.path.join(filepath,item), auto)
		elif '-u' in arg:
			argindex = arg.index('-u')
			arg.pop(argindex)
			while len(arg) != 0 and (argindex < len(arg))and(not '-' in arg[argindex]):
				if not arg[argindex][-4:] == '.vhd':
					arg[argindex] = arg[argindex] + '.vhd'
				if not arg[argindex] in allfile:
					print('ERROR: component' +  arg[argindex] + ' not found in ' + filepath+'.\n')
					exit(1)
				
				allfile.pop(allfile.index(arg[argindex]))
				arg.pop(argindex)
			writeFrame(filename)
			writeEntity(filename, topname)
			addports(filename, arg)
			for item in allfile:
				addcomponent(filename,os.path.join(filepath,item), auto)
		else:
			writeFrame(filename)
			writeEntity(filename, topname)
			addports(filename, arg)
			for item in allfile:
				addcomponent(filename,os.path.join(filepath,item), auto)
