#!/usr/bin/env python3
# pid_get.py
# Searches for the PID of a given process

from __future__ import print_function # bring the print function from Python 3 into Python 2.6+
from subprocess import call, Popen, PIPE, STDOUT

import os
import sys

# Returns: List containing the PID and other information related to that process
def get_pid_full(pscript):
  try:
    # For the start time and elapsed time (uptime): ps -eo pid,stime,etime | grep $YOUR_PID | awk '{print $2,$3}'
    pid_full = ["0","-","-"]
    pid = get_pid(pscript)
    if (pid>0):
      # Get the start and elapsed (up) times
      cmd = "ps -eo pid,stime,etime | grep " + str(pid) + " | awk '{print $2,$3}'"
      p = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT)
      p.wait() # wait for command to finish

      for line in iter(p.stdout.readline, ""):
        line_seg = line.split()
        pid_full = [str(pid),line_seg[0],line_seg[1]]
        break

    return pid_full

  except: #catch *all* exceptions
    e = sys.exc_info()
    raise e

def get_pid(pscript,param1=None):
  try:
    # Get a list of matching processes for pscript, with an exclude for
    # "pid_get" and "pid_kill" to avoid returning a second instance (created at
    # the time this command is run) to the actual process we are looking for.
    # The line splits separate out the first few characters of pscript for a
    # more exacting result.
    cmd = "ps -ef | grep -E \'[" + pscript.split()[0][0:3] + "]" + pscript.split()[0][3:] + "\' | grep -Ev 'pid_get|pid_kill'"
    p = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT)
    p.wait() # wait for command to finish
    
    pid = 0
    for line in iter(p.stdout.readline, ""):
      # Grab the CMD string and look for an exact process name match
      if (sys.version_info > (2, 8)):
        # needed to accommodate for subprocess.Popen results in python3
        line = line.decode('utf-8')
        if (len(line)==0):
          break
      line_seg = line.split()
      
      # Iterate backwards to find the process name and an exact PID match.
      # An exact PID match is found if the process name matches and if:
      # 1. A process arg is not expected and one isn't present with this PID,
      #    and this isn't someone viewing the process script in an editor; OR
      # 2. A process arg is expected and a matching arg is found with this PID.
      for i in range(len(line_seg)-1, 0, -1):
        pcmd = line_seg[i].split("/")
        if (pcmd[len(pcmd)-1]==pscript):
          #if ((param1 is None and i==len(line_seg)-1 and line_seg[i-1][:2]!="vi") or (param1 is not None and i<len(line_seg)-1 and line_seg[i+1]==param1)):
          if ((param1 is None and i==len(line_seg)-1 and line_seg[i-1][:2]!="vi") or (param1 is not None and i<len(line_seg)-2 and line_seg[i+2]==param1)):
            pid = line.split()[1].strip() # PID found
            break

    return pid

  except: #catch *all* exceptions
    e = sys.exc_info()
    raise e

def main(argv):
  script_name = os.path.basename(__file__) #the name of this Python script

  #if (len(argv)!=2):
  if (len(argv)<2):
    print("Usage: python " + script_name + " [process script name]")
    print("   or: python " + script_name + " [process script name] [?parameter]")
    sys.exit(-1)

  param1 = None
  if (len(argv)>2 and argv[2]!=""):
    param1 = argv[2]

  pid = get_pid(argv[1],param1)
  print(pid) #used by the Korn Shell script that called this file
  sys.exit(0)

if __name__ == "__main__":
  main(sys.argv[0:]) #sys.argv[0] is the name of the script
