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

# Problem:
	#component port map sequence


	

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
#	elif Fun == 'top':
#		topGen(sys.argv[2:])
#	elif Fun == 'tb':
#		tbGen(sys.argv[2:])
#	elif Fun == 'pkg':
#		pgkGen(sys.argv[2:])
#	elif Fun == 'clear':
#		vxClear()
#	elif Fun == 'version':
#		printInfo()
	else :
		print("Usage: python vxgen.py <func> <args>")
		exit(1)


if __name__ == '__main__':
    main()

