from math import *
import shutil
import os

def findArchBegin(data):
	'''
	Find the index of 'begin' of architecture, in the list of file data
	'''
	beginEnd = 0
	flag = 0
	for line in reversed(data):
		line = line.split('--',1)[0] #omit the comments
		if 'end architecture' in line:
			flag = 1
			beginEnd = beginEnd + 1
		if 'end process' in line or 'end function' in line or 'end procedure' in line: ################???
			beginEnd = beginEnd + 1
		if line[0:6] == 'begin ' or line[0:6] == 'begin\t' or line[0:6] == 'begin\n' or ' begin ' in line or \
		'\tbegin ' in line or '\tbegin\t' in line or ' begin\t' in line or ' begin\n' in line or '\tbegin\n' in line or \
		';begin ' in line or ';begin\n' in line or ';begin\t' in line:
			beginEnd = beginEnd - 1
		if beginEnd == 0 and flag == 1:
			return data.index(line)

	print("Can't find proper architerture begin, please check input file.\n")
	exit(1)

def findArchHead(data):
	for line in data:
		line = line.split('--',1)[0]
		bool1 =  line[0:13] == 'architecture ' or ' architecture ' in line or '\tarchitecture ' in line or '\tarchitecture\t' in line or ' architecture\t' in line
		bool2 = 'is' in line  #not all but enough
		if bool1 and bool2 :
			return data.index(line)
	print("Can't find proper architerture head, please check input file.\n")
	exit(1)

def findArchEnd(data): #find the last end
	for line in reversed(data):
		line = line.split('--',1)[0] #omit the comments
		if line[0:4] == 'end ' or line[0:4] == 'end\t' or ' end ' in line or '\tend ' in line or '\tend\t' in line or ' end\t' in line:
			return data.index(line)
	print("Can't find proper architerture end, please check input file.\n")
	exit(1)

def addcounter(writename, countnum):

	'''
	Required: the last line of the file should be end architecture
	'''
	with open(writename, 'r') as file:
		data = file.readlines()
	datapt = findArchBegin(data)
	countname = 'count' + str(countnum)
	countwidth = int(ceil(log(countnum, 2)))
	data.insert(datapt, 'signal ' + countname + ': unsigned(' + str(countwidth - 1) + ' downto 0);\n')
	datapt = datapt + 2
	with open(os.environ["VHDLXGEN_PATH"] + '/data/count.vd', 'r') as file:
		countdata = file.readlines()
	for line in countdata:
		line = line.replace('$count_name', countname)
		line = line.replace('#count_num', str(countnum))
		line = line.replace('#count_width', str(countwidth))
		data.insert(datapt, line)
		datapt = datapt + 1
	with open(writename, 'w') as file:
		for line in data:
			file.write(line)


def addclkdiv(writefile, divnum):
	'''
	add odd divied clk to writefile
	'''
	if divnum % 2 == 0:
		sfile = os.environ["VHDLXGEN_PATH"] + '/data/sclkdiveven.vd'
		cfile = os.environ["VHDLXGEN_PATH"] + '/data/clkdiveven.vd'
	else:
		sfile = os.environ["VHDLXGEN_PATH"] + '/data/sclkdivodd.vd'
		cfile = os.environ["VHDLXGEN_PATH"] + '/data/clkdivodd.vd'
	divwidth = ceil(log(divnum, 2))
	clkname = 'clk_d' + str(divnum)
	with open(writefile, 'r') as file:
		data = file.readlines()
	datapt = findArchBegin(data)
	with open(sfile, 'r') as file:
		sdata = file.readlines()
	for line in sdata:
		line.replace('#div', str(divnum))
		line.replace('#width', str(divwidth - 1))
		line.replace('$name',clkname)
		data.insert(datapt, line)
		datapt = datapt + 1

	datapt = datapt + 1 #after begin
	with open(cfile, 'r') as file:
		cdata = file.readlines()
	for line in cdata:
		line = line.replace('#div', str(divnum))
		line = line.replace('#width', str(divwidth - 1))
		line = line.replace('$name',clkname)
		data.insert(datapt, line)
		datapt = datapt + 1
	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)
		


def addfsm(writefile, arg):
	states = []
	statenum = 0
	if len(arg) == 1 and arg[0].isdigit():
		statenum = int(arg[0])
		for i in range(statenum):
			states.append('s' + str(i))
	else:
		states = arg
		statenum = len(arg)
	with open(writefile, 'r') as file:
		data = file.readlines()
	hpt = findArchHead(data)
	bpt = findArchBegin(data)
	hpt = hpt + 1
	data.insert(hpt, 'type state_type is (' + str(states)[1:-1].replace('\'','') + ');\n')
	hpt = hpt - 1
	data.insert(bpt, '-- signals for FSM\n')
	bpt = bpt + 1
	data.insert(bpt, 'signal current_state, next_state: state_type;\n')
	bpt = findArchBegin(data) + 1
	with open(os.environ["VHDLXGEN_PATH"] + '/data/fsm.vd', 'r') as file: 
		cdata = file.readlines()
	for line in cdata:
		data.insert(bpt, line)
		bpt = bpt + 1
	for s in states:
		data.insert(bpt, '\t\twhen ' + s + ' =>\n')
		bpt = bpt + 1
		data.insert(bpt, '\t\t\t\n')
		bpt = bpt + 1
	data.insert(bpt, '\tend case;\n')
	bpt = bpt + 1
	data.insert(bpt, 'end process;\n')
	bpt = bpt + 1
	data.insert(bpt, '--------------------------------------------</FSM>\n')
	bpt = bpt + 1
	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)

def addreg(writefile, mode):
	with open(writefile, 'r') as file:
		data = file.readlines()
	pt = findArchEnd(data)
	with open(os.environ["VHDLXGEN_PATH"] + '/data/'+mode+'.vd', 'r') as file: 
		for line in file:
			data.insert(pt, line)
			pt = pt + 1
	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)


def getEntityHead(data):
	'''
	in: file data
	out: entity data
	'''
	cpdata = []
	flag = 0
	for line in reversed(data):
		line =  line.split('--',1)[0] #omit the comments
		if 'end entity' in line:
			cpdata.append(line)
			flag = 1
		elif 'entity ' in line:
			cpdata.append(line)
			break
		elif flag == 1:
			cpdata.append(line)
	

	if len(cpdata) == 0:
		print('Can\'t find entity declearation. Please check input file.')
		exit(1)
	cpdata.reverse()
	
	return cpdata

def getPorts(data):
	'''
	in: entity data
	out: port names and widths
	'''
	name = []
	width = []
	ports = {}
	for line in data:
		line =  line.split('--',1)[0] #omit the comments
		if ':' in line:
			name.append(line.split(':')[0].strip())
			str2 = line.split(':')[1]
			if 'downto' in str2:
				width.append(int(int(filter(str.isdigit,str2.split('downto')[0])) + 1))		#e.g. (7 downto 0) -->  8
			else:
				width.append(1)
	if len(name) == 0:
		print('Warning: Master file or component has no ports.')
		
	for i in range(len(name)):
		ports[name[i]] = width[i]
	return ports

def getSignals(data):
	signals = []
	width = []
	sig = {}
	for line in data:
		if 'signal ' in line:
			signals.append(line.split('signal')[1].split(':')[0].strip())
			str2 = line.split(':')[1]
			if 'downto' in str2:
				width.append(int(int(filter(str.isdigit,str2.split('downto')[0])) + 1))		#e.g. (7 downto 0) -->  8
			else:
				width.append(1)
	for i in range(len(signals)):
		sig[signals[i]] = width[i]
	return sig


def addcomponent(writefile, componentf, auto):
	with open(writefile, 'r') as file:
		data = file.readlines()
	with open(componentf, 'r') as file:
		cdata = file.readlines()
	pt = findArchHead(data) + 1
	
	entityhead = getEntityHead(data)
	
	
	
	centityhead = getEntityHead(cdata)
	masterSignals = getSignals(data)
	portsDic = getPorts(entityhead)
	cportsDic = getPorts(centityhead)
	componentName = os.path.split(componentf)[1][:-4]
	# write component declearations
	for line in centityhead:
		line = line.replace('entity', 'component')
		data.insert(pt, line)
		pt = pt + 1

	ptbb = findArchBegin(data)
	ptb = ptbb + 1
	# write port map
	if auto:
		
		data.insert(ptb, 'inst_' + componentName + ': port map(\n')
		ptb  = ptb + 1
		signalsToRename = []
		for port in cportsDic:
			if port in portsDic :
				if not cportsDic[port] == portsDic[port]: #width !=
					signalsToRename.append(port)
			elif port in masterSignals:
				if not cportsDic[port] == masterSignals[port]:
					signalsToRename.append(port)
				
		for port in cportsDic:
			if port in signalsToRename:
				data.insert(ptb, '\t'+ port +'\t=> '+port+'_'+componentName+',\n')
				ptb = ptb + 1
			else:
				data.insert(ptb, '\t'+ port +'\t=> '+port+',\n')
				ptb = ptb + 1
		data[ptb - 1] = data[ptb - 1][:-2] + '\n' # delete last ,
		data.insert(ptb, ');\n\n')
		for sig in signalsToRename:
			sigwidth = int(cportsDic[sig])
			if sigwidth == 1:
				data.insert(ptbb, 'signal ' + sig + '_'+componentName+': std_logic;\n')
				ptbb = ptbb + 1
			else:
				data.insert(ptbb, 'signal ' + sig + '_'+componentName+': std_logic_vector('+ str(sigwidth-1) +' downto 0);\n')
				ptbb = ptbb + 1

	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)




def addComponents(arg):
	'''
	function entry for 'add'
	'''
	if len(arg) == 0 :
		print('Input arguments error!\nUsage:vxgen add <filename> <component> <arg> ...\n')
		exit(1)
	entityname = arg.pop(0)
	if '-f' in arg:
		filepath = arg.pop(arg.index('-f')+1)
		arg.pop(arg.index('-f'))
	else:
		filepath = os.getcwd()
	if entityname[-4:] == '.vhd':
		filename = filepath + '/' + entityname
	else :
		filename = filepath + '/' + entityname + '.vhd'
	if not os.path.exists(filename):
		writeframe(filename, entityname)
	elif len(arg) == 0 :
		print('Input arguments error!\nUsage:vxgen add <filename> <component> <arg> ...\n')
		exit(1)
	else:
		component = arg.pop(0)
		if component == 'counter':
			if len(arg) == 0:
				print('Input arguments error!\nUsage:vxgen add <filename> counter <num> ...\n')
				exit(1)
			for item in arg:
				if not item.isdigit():
					print('Input arguments error!\nUsage:vxgen add <filename> counter <num> ...\n')
					exit(1)
				else:
					addcounter(filename, int(item))
		elif component == 'clk_div':
			if len(arg) == 0:
				print('Input arguments error!\nUsage:vxgen add <filename> clk_div <num> ...\n')
				exit(1)
			for item in arg:
				if not item.isdigit():
					print('Input arguments error!\nUsage:vxgen add <filename> clk_div <num> ...\n')
					exit(1)
				else:
					addclkdiv(filename, int(item))
		elif component == 'fsm':
			if len(arg) == 0:
				print('Input arguments error!\nUsage:vxgen add fsm <num> {<args>} ...\n')
				exit(1)
			addfsm(filename, arg)
		elif component == 'reg':
			if len(arg) == 0:
				addreg(filename, 'ps');
			else:
				for item in arg:
					addreg(filename, item)			
		else:
			libpath = os.environ["VHDLXGEN_PATH"] + '/lib'
			if component[:-4] == '.vhd':
				libname = libpath + '/' + component 
				currentname = os.getcwd() + '/' + component
			else :
				libname = libpath + '/' + component + '.vhd'
				currentname = os.getcwd() + '/' + component + '.vhd'
			autocon = True
			if '-n' in arg:
				autocon = False
			if os.path.exists(currentname):
				addcomponent(filename, currentname, autocon)
			elif os.path.exists(libname):
				shutil.copyfile(libname, currentname)
				addcomponent(filename, currentname, autocon)
			else :
				print('Can\'t find anyone of following files:\n%s\n%s\n'%(currentname, libname))
				exit(1)