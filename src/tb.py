import sys
import os
#import os.path.join as join
from gen import *
from add import *


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
		print('ERROR: ' +filename + ' not found in '+filepath)
		exit(1)
	fullname = os.path.join(filepath , filename)
	tbfullname = os.path.join(filepath,'tb_' + filename)
	writeFrame(tbfullname)
	writeEntity(tbfullname, 'tb_' + filename[:-4])
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
