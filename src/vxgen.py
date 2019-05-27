# 2019.5.28 start
import sys


def main():
	if len(sys.argv) < 1:
		print("Usage: python vxgen.py <func> <args>")
		exit(1)
	Fun =  sys.argv[1]
	if Fun == 'gen':
		generation(sys.argv[2:])
	else if Fun == 'add':
		addComponents(sys.argv[2:])
	else if Fun == 'top':
		topGen(sys.argv[2:])
	else if Fun == 'tb':
		tbGen(sys.argv[2:])
	else if Fun == 'pkg':
		pgkGen(sys.argv[2:])
	else if Fun == 'clear':
		vxClear()
	else:
		printInfo()

if __name__ == '__main__':
    main()
