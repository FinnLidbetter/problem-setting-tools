#!/bin/bash

# Replace invocations with commands to execute each solution.
ANS_INVOCATION="java Solution"
INVOCATIONS=("java Solution" "python3 solution.py")


POSITIONAL_ARGS=()
CUSTOM_VALIDATOR=0

while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--custom-validator)
      CUSTOM_VALIDATOR=1
      shift # past argument
      ;;
    -h|--help)
      echo "Usage: find-discrepancies.sh NUM_CASES [-c|--custom-validator]"
      echo "\tModify the ANS_INVOCATION and INVOCATIONS variables to let this script know how to run solutions."
      echo "\tMust be used in conjunction with a data_generator that produces files named tmp-test-case.in and tmp-test-case.desc."
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

NUM_CASES=$POSITIONAL_ARGS[0]
bad_cases=0


for (( test_case_num=1; test_case_num<=$NUM_CASES; test_case_num++ ));
do
    echo "Running test ${test_case_num}/${NUM_CASES}. ${bad_cases} disagreements."
    python3 xtra/data_gen.py --test-name tmp-test-case
    ${ANS_INVOCATION} < tmp-test-case.in > tmp-test-case.ans
    is_bad=0
    for inv_index in ${!INVOCATIONS[@]};
    do
        if [ $CUSTOM_VALIDATOR -eq 1 ];
        then
            ${INVOCATIONS[$inv_index]} < tmp-test-case.in | python3 output_validators/validator.py tmp-test-case.in tmp-test-case.ans "invocation_${inv_index}_"
            ret_val=$?
            if [ $ret_val -ne 42 ];
            then
                mv "invocation_${inv_index}_judgemessage.txt" "bad_case_${bad_cases}_${inv_index}_judgemessage.txt"
                echo "Invocation '${INVOCATIONS[${inv_index}]}' disagrees on bad_case_${bad_cases}.in"
                is_bad=1
            fi
        else
            ${INVOCATIONS[$inv_index]} < tmp-test-case.in | diff -bB tmp-test-case.ans -
            ret_val=$?
            if [ $ret_val -ne 0 ];
            then
                echo "Invocation '${INVOCATIONS[${inv_index}]}' disagrees on bad_case_${bad_cases}.in"
                is_bad=1
            fi
        fi
    done
    if [ $is_bad -eq 1 ];
    then
        cp tmp-test-case.in "bad_case_${bad_cases}.in"
        cp tmp-test-case.ans "bad_case_${bad_cases}.ans"
        cp tmp-test-case.desc "bad_case_${bad_cases}.desc"
        bad_cases=$((bad_cases + 1))
    fi
done
if [ $bad_cases -eq 0 ];
then
    echo "All good :)"
fi

