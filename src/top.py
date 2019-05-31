import sys
import os
from gen import *
from add import *



def is_component(a):
	if a[-4:] == '.vhd' and (not 'tb_' in a) and(not '_TOP' in a):
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
		arg.pop(arg.index('-f'))
		auto = False
	else:
		auto = True

	if len(arg) == 0:
		filename = filepath + '/'+ filepath.split('/')[-1] + '_TOP.vhd'
		topname = filepath.split('/')[-1] + '_TOP'
		print('Info: filename no specified, use ' + topname + '.vhd\n')
	else:
		filename = arg.pop(0)
		if not len(filename.split('/')) == 1:
			print('Warning: <filename> should not contain path. Use -f <folder> to change.\nWarning: <folder> using default: '+os.getcwd()+'\n')
		if not filename[-4:] == '.vhd':
			topname = filename[:-4]
			filename = filepath + filename + '.vhd'
		else:
			topname = filename
			filename = filepath + filename
	allfile = filter(is_component, allfile)

	if len(arg) == 0:
		writeframe(filename, topname)
		for item in allfile:
			addcomponent(filename,filepath + '/'+item, auto)
	else:
		if '-u' in arg and '-c' in arg:
			print('Can\'t specify -c and -u at the same time.')
			exit(1)
		if '-c' in arg:
			allfile1 = []
			argindex = arg.index('-c')
			arg.pop(argindex)
			while not '-' in arg[argindex]:
				if not arg[argindex][-4:] == '.vhd':
					arg[argindex] = arg[argindex] + '.vhd'
				if not arg[argindex] in allfile:
					print('ERROR: component' +  arg[argindex] + ' not found in ' + filepath+'.\n')
					exit(1)
				allfile1.append(arg[argindex])
			writeframe(filename, topname)
			addports(filename, arg)
			for item in allfile1:
				addcomponent(filename,filepath + item, auto)
		elif '-u' in arg:
			argindex = arg.index('-u')
			arg.pop(argindex)
			while not '-' in arg[argindex]:
				if not arg[argindex][-4:] == '.vhd':
					arg[argindex] = arg[argindex] + '.vhd'
				if not arg[argindex] in allfile:
					print('ERROR: component' +  arg[argindex] + ' not found in ' + filepath+'.\n')
					exit(1)
				allfile.pop(allfile.index(arg[argindex]))
			writeframe(filename, topname)
			addports(filename, arg)
			for item in allfile:
				addcomponent(filename,filepath + item, auto)
		else:
			writeframe(filename, topname)
			addports(filename, arg)
			for item in allfile:
				addcomponent(filename,filepath + item, auto)