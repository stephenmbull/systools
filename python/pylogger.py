#!/usr/bin/python
# pylogger.py
# Simple Python file logger.
#
# Example usage:
#   sys.path.append('/opt/mysharedlibs/pylib') #path to pylogger.py
#   from pylogger import file_log
#   fl = file_log("/tmp/my_log_file.log")
#   fl.write_log("ERROR: Something went wrong!")
#

from __future__ import print_function # bring the print function from Python 3 into Python 2.6+
from datetime import datetime

import os
import sys

class file_log:
  __fname = None
  __fmode = "a"
  __dtfmt = "%Y-%b-%d %H:%M:%S"

  # File mode 'a' (default) opens the file for appending. Pass in 'w' for
  # writing (truncates the file if it already exists).
  def __init__(self, filename, file_mode=None, date_format=None):
    self.__fname = filename
    if (file_mode is not None): self.__fmode = file_mode
    if (date_format is not None): self.__dtfmt = date_format

  def set_file_mode(self, file_mode):
    self.__fmode = file_mode

  def set_date_format(self, date_format):
    self.__dtfmt = date_format

  def truncate(self):
    if (self.__fname is not None): file(self.__fname,"w").close()

  def write_log(self, log_msg):
    try:
      # 'with open' avoids the explicit close
      with open(self.__fname, self.__fmode) as log_file:
        dt = datetime.now().strftime(self.__dtfmt)
        log_file.write(dt+" "+log_msg+"\n")

    except: #catch *all* exceptions
      print("Exception in " + os.path.basename(__file__)) #this script file name
      e = sys.exc_info()
      raise e, e[1]
