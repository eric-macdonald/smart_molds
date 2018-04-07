#!/Users/eric.w.macdonald/miniconda2/bin/python
import os
import sys
import re
#  /Library/Frameworks/Python.framework/Versions/2.7/bin/python

if (len(sys.argv)!= 2):
    print "need file name"
    exit()

infile =  open(sys.argv[1], 'r')
outfile = "new_" + str(sys.argv[1]) 
outfile = open(outfile, 'w')


for line in infile:
    match1 = re.search(r"\[datetime.datetime\((.*), (.*), (.*), (.*), (.*), (.*), (.*)\), (.*)\]", line)
    match2 = re.search(r"\[datetime.datetime\((.*), (.*), (.*), (.*), (.*), (.*)\), (.*)\]", line)
    match3 = re.search(r"\[datetime.datetime\((.*), (.*), (.*), (.*), (.*)\), (.*)\]", line)
    if(match1 is not None):
        match4 = re.search("([0-9][0-9][0-9][0-9][0-9][0-9])", match1.group(7))
        if(match4 is None):
            match5 = re.search(r"([0-9][0-9][0-9][0-9][0-9])", match1.group(7))
            if(match5 is None):
                micro = "00"+match1.group(7)
            else:
                micro = "0"+match1.group(7)
        else:
            micro = match1.group(7)
        outline = match1.group(1) + "-" +  match1.group(2) + "-" +  match1.group(3) + "T" +  match1.group(4) + ":" +  match1.group(5) + ":" +  match1.group(6) + "." +  micro + "," +  match1.group(8) + "\n"
        outfile.write(outline)
    elif(match2 is not None):
        print line
        outline = match2.group(1) + "-" +  match2.group(2) + "-" +  match2.group(3) + "T" +  match2.group(4) + ":" +  match2.group(5) + ":" +  match2.group(6) + ".000000," +  match2.group(7) + "\n"
        outfile.write(outline)
        print outline
    elif(match3 is not None):
        outline = match3.group(1) + "-" +  match3.group(2) + "-" +  match3.group(3) + "T" +  match3.group(4) + ":" +  match3.group(5) + ":0.0," +  match3.group(6) + "\n"
        outfile.write(outline)
        print line
        print outline
    else:
        print line
        print "bad line"

infile.close()
outfile.close()
