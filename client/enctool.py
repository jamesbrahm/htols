import codecs
import argparse
import sys

def argstuff():
	parser = argparse.ArgumentParser()
	parser.add_argument("MODE", choices=["enc", "dec"])
	parser.add_argument("FILE")
	global args
	args = parser.parse_args()

def enc(line):
	line = line.encode("utf-8")
	enctext = codecs.encode(line, "hex").decode("utf-8")
	revtext = enctext[::-1]
	return revtext

def dec(line):
	reversed = line[::-1]
	decoded = codecs.decode(reversed, "hex").decode("utf-8")
	return decoded

def main():
	argstuff()
	try:
		targetfile = open(args.FILE, "r")
	except:
		print("Couldn't open file "+args.FILE)
		sys.exit()
	targetlines = targetfile.readlines()
	for line in targetlines:
		line = line.rstrip()
		if(args.MODE == "enc"):
			new = enc(line)
			print(new)
		elif(args.MODE == "dec"):
			new = dec(line)
			print(new)
		else:
			print("uh oh")

main()
