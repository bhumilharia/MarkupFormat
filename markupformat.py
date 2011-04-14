import sys;

path = sys.argv[1];
fname = sys.argv[2];

blockType='';
tagLevel=-1;
longstring='';

#Functions
def formatFile(path,fname):
	inf, outf, EOF = initIO(path,fname);
	count=0;
	while(count< EOF):
		block = readBlock(inf, EOF);
		write(block, outf);
		count = inf.tell();
	outf.close();
	return;

def initIO(path, fname):
	#Open Files
	inf = open(path+fname, 'r');
	outf = open(path +"output" + fname, 'w');
	
	#Get EndOfFile Position
	inf.seek(0,2);
	EOF = inf.tell();
	inf.seek(0,0);
	# Eof found
	return inf, outf, EOF;

def indent():
	i= 0;
	dataIndent=0;
	indents='';
	global blockType, tagLevel;

	if blockType=="data" : 
		dataIndent=1;
	elif blockType == "start" :
		tagLevel += 1;		#Increment tagLevel coz tag opened

	while i < tagLevel + dataIndent:
		indents+="   ";
		i+=1;

	if blockType=="end":		#Decrement tagLevel coz tag closed
		tagLevel -= 1;
	else: pass;

	return indents;

def readUpto(char,inf, EOF):
	finput, fc = '', '';
	count= inf.tell();
	while ((fc != char) and count < EOF-1):
		finput += fc;
		fc = inf.read(1);
		count+=1;
	#End traversal

	if fc=='>': finput += fc;				#complete tag, if tag
	else:
		if count != EOF : inf.seek(count-1,0);		#go back one char ('<')
	return finput;

def readBlock(inf, EOF):
	#Traverse through File one black at a time
	global tagLevel, blockType;

	block = inf.read(1);
	if block=='<':					#Tag
		block += readUpto('>', inf, EOF);	#Read upto '>'
		if block[0:2] =='</':			#End Tag
			
			blockType="end";
		else:					#Start tag
			#tagLevel +=1;
			blockType="start";
	else:						#No tag/ data
		block += readUpto('<', inf, EOF);
		blockType="data";
		#tagLevel +=1;
	return block;

def write(block, outf):
	global tagLevel, longstring;
	line = indent() + block + "\n";
	longstring += line;
	outf.write(line);
	return;	

formatFile(path, fname);
