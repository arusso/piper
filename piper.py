#!/usr/bin/python

# author: arusso@berkeley.edu
# date:   09-Feb-2012
# purpose: small library to help clean up the code needed to run shell commands
#          and retrieve the output in python

from subprocess import Popen,PIPE
from shlex import split

class Piper:
    """Piper takes a shell statement, including with a PIPE, executes the statement and returns the data, taking advantage of the subprocess module."""

    
    def run(self,line):
        """
        Takes a command line, runs it and returns the stdout
        """
        # first, lets take apart the pipe
        tokens=split(line)
        statement=0
        cmds = []
        cmds.append("")
        for token in tokens:
            # add the tokens to the current statement until we reach a |
            
            if token == "|":
                cmds.append("")
                statement+=1
            else:
                if cmds[statement]!="":cmds[statement]+=","
                cmds[statement]+=token
        #print cmds

        # get ready to do the "real" work
        idx=0
        processes=[]
        processes.append(Popen(cmds[0].split(','),stdout=PIPE))

        # build our processes, then link the previous stdout with the current stdin
        for cmd in cmds[1:]:
            processes.append(Popen(cmd.split(','),stdin=processes[idx].stdout,stdout=PIPE))
            idx+=1

            
        # return stdout from the final process we ran
        return processes[-1].communicate()[0]

if __name__=="__main__":
    line="lsof -T"
    print "testing run(line) function with line=\""+line+"\""
    p=Piper()
    out=p.run(line)
    
    # the comma is to keep it from printing the newline
    print out,
