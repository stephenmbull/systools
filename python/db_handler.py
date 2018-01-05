#!/usr/bin/python
# Database I/O handler for Python scripts. 

from __future__ import print_function # bring the print function from Python 3 into Python 2.6+
from subprocess import call, Popen, PIPE, STDOUT

import sys

class db_io:
  __SQLPLUS = '. /myfilepath/mysqlplus.sourcefile' # file containing database connection information; modify accordingly
  __conn_str = ''
  __err_msg = ""

  def __init__(self):
    self.__conn_str = self.__get_db_connect_string()

  def __get_db_connect_string(self):
    p = Popen(self.__SQLPLUS + '\necho $SECURITY', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    p.wait() #wait for the command to finish
    conn_str = ''
    for line in iter(p.stdout.readline, ''):
      conn_str = line.split()[0:1][0].strip()
      break
    return conn_str

  def exec_sql(self, sql):
    try:
      p = Popen(['sqlplus','-S',self.__conn_str], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
      p.stdin.write('set heading off   pause off   echo off   feedback off   pagesize 0\n')
      p.stdin.write('WHENEVER SQLERROR EXIT FAILURE\n')

      p.stdin.write(sql)
      result = p.communicate()[0].strip() #communicate() closes the stream

      try:
        # Raise exception for an Oracle error
        idx = result.index("ORA-") #start pos if search string is found
        self.__err_msg = result[idx:] + "\\nSQL: " + sql
        raise Exception
      except ValueError:
        e = sys.exc_info()
        # Ignore ValueError; just means error string wasn't found in result

      return result
    except: #catch *all* exceptions
      print("Exception in " + os.path.basename(__file__)) #this script file name
      e = sys.exc_info()
      #raise e, e[1]
      raise e, self.__err_msg #not an ideal way to raise a custom exception, but this will work for now

    return 0
