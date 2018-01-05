#!/bin/ksh
# pid_kill.ksh
# Kills the PID of a given running process (arg $1)

usage_error() {
  echo " "
  echo "Usage: $0 [process name] [?arg]"
  echo " "
  exit 1
}

#Validate the expected arguments
if [[ "$#" -lt 1 ]]; then
  usage_error
fi

lib_path="/opt/mysharedlibs/pylib/" # change to point to this file's location

proc_name=$1
arg=""

if [[ "$#" -gt 1 ]]; then
  arg=$2
fi

pid=$(python $lib_path/pid_get.py $proc_name $arg)
exit_val=$?

if [[ $exit_val = 0 && $pid > 0 ]]; then
  stdout=$(kill $pid)
  exit_val=$(echo $?)
fi

echo $pid
exit $exit_val
