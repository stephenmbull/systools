#!/bin/ksh
# pid_get_wrapper.ksh
# A wrapper to pid_get.py (which returns either a 0 when no PID is found or a
# real PID value). This wrapper will exit with a non-zero (fail) or zero
# (success) respectively.

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

if [[ $exit_val = 0 && $pid = 0 ]]; then
  exit_val=1 #fail
fi

echo $pid
exit $exit_val
