#!/bin/zsh

# Place this file in data/secret along with some program or executable.
# Modify the INVOCATION variable to match how the program should be run.

INVOCATION="java Solution"

for in_file in *.in; 
do
    [ -f "$in_file" ] || break
    ${INVOCATION} < "${in_file}" > "${in_file%.in}.ans"
done
