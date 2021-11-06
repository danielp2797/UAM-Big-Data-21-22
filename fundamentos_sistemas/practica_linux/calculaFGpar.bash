#!/bin/bash
./factorial.bash 1000 > /dev/null &
./factorial.bash 1001 > /dev/null &
./factorial.bash 1002 > /dev/null &
./factorial.bash 1003 > /dev/null &
wait
