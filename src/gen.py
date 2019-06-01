import time
import platform
import getpass
import os
#-------------------------------------------
# function:
	# genaration():
	# writeframe(writefile, entityname)
	# addports(writefile, arg)
#-------------------------------------------

def writeFrame(writefile):
	'''
	Write title and libaraies.
	'''
	confpath = os.environ["VHDLXGEN_PATH"] + '/conf'
	title = []
	lib = []
	with open(writefile, 'w+') as file:
		file.write("--------------------------------------------------\n")
		with open(confpath + '/title.conf', 'r') as f:
			for line in f:
				line = line.strip()
				if line[0] != '#':
					if 'Time' in line:
						if len(line.split(':')) == 1:
							towrite = '-- Creat time: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
							file.write(towrite)
						else:
							file.write('-- '+ line+ '\n')
						
					elif 'Engineer' in line:
						if len(line.split(':')) == 1:
							file.write('-- Engineer: ' + getpass.getuser() + '\n')
						else:
							file.write('-- '+ line+ '\n')
					elif 'Platform' in line:
						if len(line.split(':')) == 1:
							file.write('-- Platform: ' + platform.uname()[0] + '\n')
							
						else:
							file.write('-- '+ line+ '\n')
					else:
						file.write('-- '+ line+ '\n')
		file.write("--------------------------------------------------\n\n\n\n")
		with open(confpath + '/library.conf', 'r') as f:
			for line in f:
				line = line.strip()
				if line[0] != '#':
					file.write( line+ '\n')

def writeEntity(writefile, entityname):
	'''
	Write Entity framwork
	'''
	with open(writefile, 'a') as file:
		file.write('\nentity ' + entityname + ' is\n' + 'port(\n);\nend entity;\n\n')
		file.write('architecture behaviral of '+ entityname + ' is\n\n' + 'begin\n\n' + 'end architecture;')


def addports(writefile, arg):
	'''
	Add ports as specified in arg
	'''
	pi = []
	po = []
	pio = []
	pstate = 0
	for item in arg:
		if pstate == 0:
			if item == '-i':
				pstate = 1
			elif item == '-o':
				pstate = 2
			elif item == '-io':
				pstate = 3
			else:
				print("Error: arguments error while adding ports!Please check the command\n")
				exit(1)
		elif pstate == 1:
			if item == '-i':
				pstate = 1
			elif item == '-o':
				pstate = 2
			elif item == '-io':
				pstate = 3
			else:
				pi.append(item)
		elif pstate == 2:
			if item == '-i':
				pstate = 1
			elif item == '-o':
				pstate = 2
			elif item == '-io':
				pstate = 3
			else:
				po.append(item)
		else :
			if item == '-i':
				pstate = 1
			elif item == '-o':
				pstate = 2
			elif item == '-io':
				pstate = 3
			else:
				pio.append(item)
	
	with open(writefile, 'r') as file:
		data = file.readlines()

	datapt = 0
	for line in data:
		if 'port(' in line:
			datapt = data.index(line) + 1
	flag = 0
	for item in pi:
		if flag == 0:
			if item.isdigit():
				print("Error: arguments error while adding ports! Please check the command\n")
				exit(1)
			else:
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
				flag = 1
		else:    #flag == 1
			
			if item.isdigit():
				num = int(item)
				if num == 1:
					data[datapt - 1] = data[datapt - 1]+ '\t: in\tstd_logic;\n'
				else:
					data[datapt - 1] = data[datapt - 1]+ '\t: in\tstd_logic_vector(' + str(num - 1) + ' downto 0);\n'
				flag = 0
			else :
				data[datapt - 1] = data[datapt - 1]+'\t: in\tstd_logic;\n'
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
	if flag == 1:
		data[datapt - 1] = data[datapt - 1]+'\t: in\tstd_logic;\n'
	flag = 0
	for item in po:
		if flag == 0:
			if item.isdigit():
				print("Error: arguments error while adding ports! Please check the command\n")
				exit(1)
			else:
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
				flag = 1
		else:    #flag == 1
			
			if item.isdigit():
				num = int(item)
				if num == 1:
					data[datapt - 1] = data[datapt - 1]+ '\t: out\tstd_logic;\n'
				else:
					data[datapt - 1] = data[datapt - 1]+ '\t: out\tstd_logic_vector(' + str(num - 1) + ' downto 0);\n'
				flag = 0
			else :
				data[datapt - 1] = data[datapt - 1]+'\t: out\tstd_logic;\n'
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
	if flag == 1:
		data[datapt - 1] = data[datapt - 1]+'\t: in\tstd_logic;\n'
	flag = 0
	for item in pio:
		if flag == 0:
			if item.isdigit():
				print("Error: arguments error while adding ports! Please check the command\n")
				exit(1)
			else:
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
				flag = 1
		else:    #flag == 1
			
			if item.isdigit():
				num = int(item)
				if num == 1:
					data[datapt - 1] = data[datapt - 1]+ '\t: inout\tstd_logic;\n'
				else:
					data[datapt - 1] = data[datapt - 1]+ '\t: inout\tstd_logic_vector(' + str(num - 1) + ' downto 0);\n'
				flag = 0
			else :
				data[datapt - 1] = data[datapt - 1]+'\t: inout\tstd_logic;\n'
				data.insert(datapt, '\t' + item)
				datapt = datapt + 1
	if flag == 1:
		data[datapt - 1] = data[datapt - 1]+'\t: in\tstd_logic;\n'

	if not (len(pi) == 0 and len(po) == 0 and len(pio) == 0):
		data[datapt - 1] = data[datapt - 1][:-2] + '\n' #delete last ;
	
	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)




def generation(arg):
	'''
	function entry for 'gen'
	'''
	if len(arg) == 0 or '-' in arg[0]:
		print('Info: file name not specified. Use \'a_vhdl_file\' :)\n')
		filepath = os.getcwd()
		entityname = 'a_vhdl_file'
	else:
		[entitypath, entityname] = os.path.split(arg.pop(0))
		if not entitypath == '':
			filepath = entitypath
		else:
			filepath = os.getcwd()
	if entityname[-4:] == '.vhd':
		filename = filepath + '/' + entityname
	else:
		filename = filepath + '/' + entityname + '.vhd'
	writeFrame(filename)
	writeEntity(filename, entityname)
	addports(filename,arg)
