#!/usr/bin/env bash

LIMIT=4
problem_dir_indicators=("problem_statement" "data" "submissions" "problem.yaml")

problemset_dir=$(pwd)
if [ $# -eq 0 ] 
then
    counter=0
    while [ $counter -lt $LIMIT ]
    do
        counter=$((counter+1))
        echo "Checking candidate problemset dir '$(pwd)'"
        for problem_dir_indicator in $problem_dir_indicators
        do
            result=$(find . -mindepth 2 -maxdepth 2 | grep -cim1 "${problem_dir_indicator}$")
            if [ $result -eq 1 ]
            then
                problemset_dir="$(pwd)"
                counter=$LIMIT
                break
            else
                pushd .. > /dev/null
            fi
        done
    done
else
    problemset_dir=$1
fi

set -x

docker run --rm -v ""$problemset_dir":/work" -it finnlidbetter/problemtools-arm-full
