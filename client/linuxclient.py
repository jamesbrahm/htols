# Imports
import subprocess
import codecs
import argparse

def argstuff():
	parser = argparse.ArgumentParser()
	parser.add_argument("TARGET")
	global args
	args = parser.parse_args()

# Obfuscation
def dec(line):
	reversed = line[::-1]
	decoded = codecs.decode(reversed, "hex").decode("utf-8")
	return decoded

# Scoring functions

def scoreVuln(vuln):
	global pointGainLines
	global pointLossLines
	global totalScore


# Score Report stuff
def genReport():
	global pointGainLines
	global pointLossLines
	global totalScore
	reportlines = []
	reportlines.append("<html> <header> <title> HTOLS Scoring Report </title </header>")
	reportlines.append("<body bgcolor=black text=#00FF00>")
	reportlines.append("<center> <h1> HTOLS Scoring Report </h1>")
	reportlines.append("<p> Generated at: 55:55:55 </p>")
	reportlines.append("<h3> Score: 420 </h3> </center> <br>")
	reportlines.append("<br> <h3> # out of # for a subtotal of ## points </h3>")
	for item in pointGainLines:
		reportlines.append(item + " <br>")

	reportlines.append("<h3> # penalties assessed for # points </h3>")
	for item in pointLossLines:
		reportLines.append(item + " <br>")

	reportlines.append("</body> </html>")


	reportFile = open("ScoreReport.html", "w")
	for line in reportlines:
		reportFile.write(line)


# Misc

def getScoringData():
	vdlFile = open("scoring.dat", "r")
	enclines = vdlFile.readlines()
	vdlLines = []
	for line in enclines:
		line = line.rstrip()
		vdlLines.append(dec(line))
	return vdlLines



def main():
	argstuff()
	vdlLines = getScoringData()
	global pointGainLines
	pointGainLines = []
	global pointLossLines
	pointLossLines = []
	global totalScore
	totalScore = []
	for line in vdlLines:
		scoreVuln(line)

	genReport()

	

main()