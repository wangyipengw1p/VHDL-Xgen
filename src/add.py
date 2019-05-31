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
			# deal with the problem that multipal 'end' in one line
			beginEnd = beginEnd + len(line.split('end process')) + len(line.split('end function')) + len(line.split('end procedure')) - 3
		if line[0:6] == 'begin ' or line[0:6] == 'begin\t' or line[0:6] == 'begin\n' or ' begin ' in line or \
		'\tbegin ' in line or '\tbegin\t' in line or ' begin\t' in line or ' begin\n' in line or '\tbegin\n' in line or \
		';begin ' in line or ';begin\n' in line or ';begin\t' in line:
			# multipal begin can't be in the same line
			beginEnd = beginEnd - 1
		if beginEnd == 0 and flag == 1:
			return data.index(line)

	print("ERROR: Can't find proper architerture begin, please check input file.\n")
	exit(1)

def findArchHead(data):
	for line in data:
		line = line.split('--',1)[0]
		bool1 =  line[0:13] == 'architecture ' or ' architecture ' in line or '\tarchitecture ' in line or '\tarchitecture\t' in line or ' architecture\t' in line
		bool2 = 'is' in line  #not all but enough
		if bool1 and bool2 :
			return data.index(line)
	print("ERROR: Can't find proper architerture head, please check input file.\n")
	exit(1)

def findArchEnd(data): #find the last end
	for line in reversed(data):
		line = line.split('--',1)[0] #omit the comments
		if 'end architecture' in line:
			if 'end process' in line:
				print('ERROR: \'end process\' and \'end architecture\' in the same line. Please check the syntex.')
				exit(1)
			return data.index(line)
	print("ERROR: Can't find proper architerture end, please check input file.\n")
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
		print('ERROR: Can\'t find entity declearation. Please check input file.')
		exit(1)
	cpdata.reverse()
	
	return cpdata

def getPorts(data):
	'''
	in: port() or generic()
	out: names and widths
	'''
	name = []
	width = []
	ports = {}
	for line in data:
		line =  line.split('--',1)[0] #omit the comments
		if  ':' in line:
			for part in line.split(';')[:-1]:			#deal with [e.g. port( clk : in std_logic; rst: in std_logic;)]
				names = part.split(':')[0].split(',') #deal with multiple ports in one line, [e.g. clk, rst : in std_logic;]
				for item in names:
					name.append(item.strip())
				
				str2 = part.split(':')[1]
				if 'downto' in str2:
					for item in names:
						width.append(int(int(filter(str.isdigit,str2.split('downto')[0])) + 1))		#e.g. (7 downto 0) -->  8
				else:
					for item in names:
						width.append(1)
	
		
	for i in range(len(name)):
		ports[name[i]] = width[i]
	return ports

def getSignals(data):
	'''
	in : original file data; out: Dictionary for signals and width
	'''
	signals = []
	width = []
	sig = {}
	for line in data:
		if len(line.split('signal ')) > 2:
			print('Multi-signals in one line. Please check syntex\nStop')
			exit(1)
		if 'signal ' in line:			#multi-signals in one line is not good syntex, which is not supported
			signames = line.split('signal')[1].split(':')[0].split(',')    #deal with multiple ports in one line
			for item in signames:
				signals.append(item.strip())
			str2 = line.split(':')[1]
			if 'downto' in str2:
				for item in signames:
					width.append(int(int(filter(str.isdigit,str2.split('downto')[0])) + 1))		#e.g. (7 downto 0) -->  8
			else:
				for item in signames:
					width.append(1)
	for i in range(len(signals)):
		sig[signals[i]] = width[i]
	return sig
#ENTITY PGAND2 IS
#    GENERIC (    trise : TIME := 1 ns;
#              tfall : TIME := 1 ns ) ;
#       PORT (    a1 : IN STD_LOGIC ;
#             a0 : IN STD_LOGIC ;
#             z0 : OUT STD_LOGIC );
#END ENTITY PGAND2;
#GENERIC MAP (n =>5)
#      PORT MAP (a(0)=>d3,a(1)=>d4,a(2)=>d5,
#                           a(3)=>d6,a(4)=>d7, c=>q2);

def getGenericPart(data):
	gdata = []
	flag = False
	for line in data:
		if 'generic' in line:
			flag = True
			line = line.replace('generic','')
			line = line.replace('(','')
			gdata.append(line)
		elif 'port' in line or 'end entity' in line:
			flag = False
		else:
			if flag:
				
				gdata.append(line)
	return gdata

def getPortPart(data):
	gdata = []
	flag = False
	for line in data:
		if 'port' in line:
			line = line.replace('port','')
			line = line.replace('(','')
			flag = True
			gdata.append(line)
		elif 'generic' in line or 'end entity' in line:
			flag = False
		else:
			if flag:
				
				gdata.append(line)
	return gdata



def addcomponent(writefile, componentf, auto):
	with open(writefile, 'r') as file:
		data = file.readlines()
	with open(componentf, 'r') as file:
		cdata = file.readlines()
	pt = findArchHead(data) + 1
	
	entityhead = getEntityHead(data)
	centityhead = getEntityHead(cdata)

	masterSignals = getSignals(data)
	portsDic = getPorts(getPortPart(entityhead))
	cportsDic = getPorts(getPortPart(centityhead))
	if len(cportsDic) == 0:
		print('Warning: '+componentf+' has no ports\n')
	cgeneDic = getPorts(getGenericPart(centityhead))
	componentName = os.path.split(componentf)[1][:-4]
	# write component declearations
	for line in centityhead:
		line = line.replace('entity', 'component')
		data.insert(pt, line)
		pt = pt + 1

	
	# write port map
	if auto:
		signalsToRename = []
		signalsToAdd = []
		for port in cportsDic:
			if port in portsDic :
				if not cportsDic[port] == portsDic[port]: #width !=
					signalsToRename.append(port)
				
			elif port in masterSignals:
				if not cportsDic[port] == masterSignals[port]:
					signalsToRename.append(port)
			else:
				signalsToAdd.append(port)
		ptb  = findArchBegin(data) + 1
		ptbb = findArchBegin(data)
		data.insert(ptb, 'inst_' + componentName +':' + componentName+' ')			#+ ': port map(\n'
		ptb = ptb+1
		# insert generic map
		if len(cgeneDic) > 0:
			data.insert(ptb, 'generic map(\n')
			ptb  = ptb + 1
			for item in cgeneDic:
				data.insert(ptb, '\t' + item + ' =>,\n')
				ptb = ptb + 1
			data[ptb - 1] = data[ptb - 1][:-2] + '\n'				#delete last ,
			data.insert(ptb, ')\n')
			ptb = ptb + 1
		data.insert(ptb, 'port map(\n')
		ptb = ptb + 1
		#insert port map
		for port in cportsDic:
			if port in signalsToRename:
				# if the component has been added before, or the name confilicts with the exist signal, 
				# the tool will rename like portx portxx portxxx ...
				rename = port
				while rename in masterSignals or rename in portsDic:
					rename = rename + 'x'
				
				data.insert(ptb, '\t'+ port +'\t=> '+rename+',\n')
				ptb = ptb + 1
				sigwidth = int(cportsDic[port])
				if sigwidth == 1:
					data.insert(ptbb, 'signal ' + rename +': std_logic;\n')
					ptbb = ptbb + 1
					ptb = ptb + 1			####!!!
				else:
					data.insert(ptbb, 'signal ' + rename +': std_logic_vector('+ str(sigwidth-1) +' downto 0);\n')
					ptbb = ptbb + 1
					ptb = ptb + 1
			else:
				data.insert(ptb, '\t'+ port +'\t=> '+port+',\n')
				ptb = ptb + 1
		data[ptb - 1] = data[ptb - 1][:-2] + '\n' # delete last ,
		data.insert(ptb, ');\n\n')
		for sig in signalsToAdd:
			sigwidth = int(cportsDic[sig])
			if sigwidth == 1:
				data.insert(ptbb, 'signal ' + sig +': std_logic;\n')
				ptbb = ptbb + 1
			else:
				data.insert(ptbb, 'signal ' + sig +': std_logic_vector('+ str(sigwidth-1) +' downto 0);\n')
				ptbb = ptbb + 1

	with open(writefile, 'w') as file:
		for line in data:
			file.write(line)




def addComponents(arg):
	'''
	function entry for 'add'
	'''
	if len(arg) == 0 :
		print('ERROR: Input arguments error!\nUsage:vxgen add <filename> <component> <arg> ...\n')
		exit(1)
	[entitypath,entityname] = os.path.split(arg.pop(0))
	if not entitypath == '':
		print('Warning: <filename> should not contain path. Use -f <folder> to change.\nWarning: <folder> using default: '+os.getcwd()+'\n')
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
		print('ERROR: Input arguments error!\nUsage:vxgen add <filename> <component> <arg> ...\n')
		exit(1)
	else:
		component = arg.pop(0)
		if component == 'counter':
			if len(arg) == 0:
				print('ERROR: Input arguments error!\nUsage:vxgen add <filename> counter <num> ...\n')
				exit(1)
			for item in arg:
				if not item.isdigit():
					print('ERROR: Input arguments error!\nUsage:vxgen add <filename> counter <num> ...\n')
					exit(1)
				else:
					addcounter(filename, int(item))
		elif component == 'clk_div':
			if len(arg) == 0:
				print('ERROR: Input arguments error!\nUsage:vxgen add <filename> clk_div <num> ...\n')
				exit(1)
			for item in arg:
				if not item.isdigit():
					print('ERROR: Input arguments error!\nUsage:vxgen add <filename> clk_div <num> ...\n')
					exit(1)
				else:
					addclkdiv(filename, int(item))
		elif component == 'fsm':
			if len(arg) == 0:
				print('ERROR: Input arguments error!\nUsage:vxgen add fsm <num> {<args>} ...\n')
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
				print('ERROR: Can\'t find anyone of following files:\n%s\n%s\n'%(currentname, libname))
				exit(1)