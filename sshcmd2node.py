#!/usr/local/bin/python

import subprocess, sys, os
from threading import Thread
from re import search
 
# Node class
class Node(Thread):
    # Constructor
    def __init__(self, name, location, sshcmd):
       # Fork the thread first thing
       Thread.__init__(self)
       # Variables initialization
       self.hostname = name
       self.location = location
       self.up       = False
       self.cmd      = sshcmd 
        

    # Run method called on Thread start: check if host is up and run sshcmd
    def run(self) :
        if self.isup() :
             self.up = True
             self.cmdresult=self.sshcommand(self.cmd)
 
    # Ping the host to see if it's up
    def isup(self):
       # Is the host up?
       ping = os.popen("ping -w1 -c1 " + self.hostname, "r")
       if "0 received" in ping.read():
          return False
       else:
          return True

    # Run a command within an ssh connection to the node.
    # Return a tuple (exit status 0/1, out/err)
    # There should be a better way to do this... Something like thowing exceptions
    # and collecting them from the calling program...
    # FIXME: doesn't always catch errors from the bash command
    def sshcommand(self, command):
       if self.isup():
          cmd = subprocess.Popen( ["ssh", "%s" % self.hostname, command],
                                   shell = False, 
                                   stdout = subprocess.PIPE,
                                   stderr = subprocess.PIPE )
          # This is not a good way to look for errors
          out, err = cmd.communicate()
          exitcode=cmd.returncode
          return (exitcode, out.strip().split('\n'), err)

       else:
          return (1, self.hostname + " is down") 

## End Node class

