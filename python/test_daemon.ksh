#!/bin/ksh
# test_daemon
# Stops and starts the program assigned to $prog_name.

usage_error() {
  echo " "
  echo "Usage: $0 [start|stop]"
  echo " "
  exit 1
}

#Validate the expected arguments
if [[ "$#" -lt 1 ]]; then
  usage_error
fi

instruct=$1
lib_path="/opt/mysharedlibs/pylib/" # change to point to this file's location
prog_name="test_daemon.py"          # default program we're controlling
prog_path="/opt/progpath"           # change to point to program path

#Execute a Python program (argument dependent)
if [[ $instruct = "start" ]]; then
  #Check for a running instance of program $prog_name
  pid=$(python $lib_path/pid_get.py $prog_name)
  exit_val=$?

  if [[ $exit_val != 0 ]]; then
    echo "exception in pid_get.py"
  elif [[ $pid = 0 ]]; then
    nohup python $prog_path/$prog_name &
    sleep 2
    echo "started $prog_name"
  else
    echo "$prog_name already running (pid $pid)"
  fi
elif [[ $instruct = "stop" ]]; then
  pid=$($lib_path/pid_kill.ksh $prog_name)
  exit_val=$?

  if [[ $exit_val != 0 ]]; then
    echo "exception in pid_kill.ksh"
  elif [[ $pid > 0 ]]; then
    echo "stopped $prog_name (pid $pid)"
  else
    echo "$prog_name is not running"
  fi
else
  usage_error
fi

exit_val=$?
exit $exit_val
