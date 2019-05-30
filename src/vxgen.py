import sys
import os
from gen import *
from add import *



# Done:
# gen

# Requirement:
	#main entity shoud be by the end of the file
	# entity one line, begin one line
	# use 'end entity'
	# port(

#To do:
# generic
# width inference
# 0 downto 0
# in out
# check name

# Problem:
	#component port map sequence
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

def tbGen(arg):
	if len(arg) ==0:
		print('Usage:vxgen tb <entityname> {-q <clkFrequency>} {-d <dutycycle>} {-diff} {-pr/-nr} {-rt <rst-time>}')
		exit(1)
	if '-f' in arg:
		filepath = arg.pop(arg.index('-f') + 1)
		arg.pop(arg.index('-f'))
	else:
		filepath = os.getcwd()
	allfile = os.listdir(filepath)
	filename = arg.pop(0)
	if not filename[-4:] == '.vhd':
		filename = filename + '.vhd'
	if not filename in allfile:
		print('ERROR: ' +filename + 'not found in '+filepath)
		exit(1)
	fullname = filepath + '/' + filename
	tbfullname = filepath + '/'+'tb_' + filename
	writeframe(tbfullname, 'tb_' + filename[:-4])
	with open(tbfullname ,'r') as file:
		tbdata = file.readlines()
	popindex = 0
	for line in tbdata:
		if 'port' in line:
			popindex = tbdata.index(line)
	tbdata.pop(popindex)
	tbdata.pop(popindex)
	with open(tbfullname ,'w') as file:
		for line in tbdata:
			file.write(line)
	
	# add clk rst
	with open(tbfullname ,'r') as file:
		tbdata = file.readlines()

	if len(arg) == 0:
		pte = findArchEnd(tbdata)
		tbdata.insert(pte,'clk <= not clk after 5 ns;\nrst <= \'0\', \'1\' after 10 ns;\n')
		ptb = findArchBegin(tbdata)
		tbdata.insert(ptb, 'signal clk, rst: std_logic;\n')
	else:
		
		
		if '-d' in arg:
			if not arg[arg.index('-d')+1].isdigit():
				print('ERROR: clk duty cycle is not a number.')
				exit(1)
			duty = float(arg.pop(arg.index('-d') + 1))
			arg.pop(arg.index('-d'))
		else :
			duty = 50.;
		
		if not '-q' in arg:
			clkcycle = 10
		else:
			if not arg[arg.index('-q') + 1].isdigit():
				print('ERROR: clk frequency is not a number.')
				exit(1)
			clkf = float(arg[arg.index('-q') + 1])
			clkcycle = 1000/clkf

		
		clkt1 = clkcycle * duty / 100
		clkt2 = clkcycle - clkt1

		pte = findArchEnd(tbdata)
		ptb = findArchBegin(tbdata)

		if '-diff' in arg:
			tbdata.insert(pte,'clkn <= not clkp;\nprocess\nbegin\n\tclkp <= \'1\';\n\twait for ' + str(clkt1) +' ns;\n\tclkp <= \'0\';\n\twait for '+ str(clkt2) +' ns;\nend process;\n')
			tbdata.insert(ptb, 'signal clkn, clkp, rst: std_logic;\n')
		else:
			tbdata.insert(pte,'process\nbegin\n\tclk <= \'1\';\n\twait for ' + str(clkt1) +' ns;\n\tclk <= \'0\';\n\twait for '+ str(clkt2) +' ns;\nend process;\n')
			tbdata.insert(ptb, 'signal clk, rst: std_logic;\n')
		#rst
		pte = findArchEnd(tbdata)
		
		if '-rt' in arg:
			resettime = arg[arg.index('-rt') + 1]
			if not resettime.isdigit():
				print('ERROR: rst time is not a number.')
				exit(1)
			if '-pr' in arg:
				tbdata.insert(pte, 'rst <=\'1\', \'0\' after '+ str(resettime)+' ns;\n')
			else:
				tbdata.insert(pte, 'rst <=\'0\', \'1\' after '+ str(resettime)+' ns;\n')
		else:
			if '-pr' in arg:
				tbdata.insert(pte, 'rst <=\'1\', \'0\' after '+ str(clkcycle)+' ns;\n')
			else:
				tbdata.insert(pte, 'rst <=\'0\', \'1\' after '+ str(clkcycle)+' ns;\n')
	with open(tbfullname ,'w') as file:
		for line in tbdata:
			file.write(line)
	

	addcomponent(tbfullname, fullname, True)
		

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
	print('Version: 0.0');
	
	
	

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

