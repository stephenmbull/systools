#!/usr/bin/python
# test_daemon.py
# Dummy daemon process for testing
# Run using nohup ./test_daemon.py &

import sys

def main(argv):
  try:
    i = 0
    while True:
      i = 1

  except:
    sys.exit(1)

if __name__ == "__main__":
  main(sys.argv[0:]) #sys.argv[0] is the name of the script
