#!/usr/bin/env python3

"""
Custom output validator.

This can be run manually on a compiled java program called `SampleSubmission` with something like:
    java SampleSubmission < test_case.in | python3 validator.py test_case.in test_case.ans verdict_
If there was an error, the error message will be printed in verdict_judgemessage.txt.
The exit code of the last run can be inspected with
    echo $?
"""


from sys import stdin, argv

N_MAX = 1000000


def report_good_answer():
    exit(42)


def report_wrong_answer(message, verdict_file):
    print(message, file=verdict_file)
    exit(43)


def is_eof(input_stream):
    line = input_stream.readline()
    if line != "":
        return False
    return True


def read_input(input_stream, verdict_file):
    """Parse the input and return the values in a useful format."""
    try:
        n = int(input_stream.readline())
        return n
    except Exception as e:
        report_wrong_answer(
            'Input could not be read. {}'.format(str(e)), verdict_file)


def read_output(input_stream, verdict_file):
    try:
        line = input_stream.readline()
        tokens = []
        while line:
            tokens.extend(line.split())
            if len(tokens) > N_MAX:
                report_wrong_answer('Too many tokens in output', verdict_file)
            line = input_stream.readline()
        if len(tokens) < 1:
            report_wrong_answer('No tokens in output', verdict_file)
        for token in tokens:
            # If parsing integers, make sure that they do not have too many digits.
            if len(token) > len(str(N_MAX)):
                report_wrong_answer('Some token has too many characters to be valid.', verdict_file)
        # Do something with the tokens here
        return []
    except Exception as e:
        report_wrong_answer('Output could not be read: {}'.format(str(e)), verdict_file)


def validate(input_values, output_values):
    """Perform validation of the output for the given input."""
    raise ValueError("Invalid solution.")

with open(argv[1], "r") as filein, \
        open(argv[2], "r") as fileans, \
        open(argv[3] + "judgemessage.txt", "w") as verdict_file:
    
    input_values = read_input(filein, verdict_file)

    judge_output = read_output(fileans, verdict_file)

    try:
        validate(input_values, judge_output)
    except Exception as judge_err:
        raise Exception(
            'Something has gone horribly wrong. '
            f'Judge solution is not valid: {str(judge_err)}.'
        )

    contestant_output = read_output(stdin, verdict_file)
    try:
        validate(input_values, contestant_output)
    except ValueError as contestant_err:
        report_wrong_answer(f'Incorrect submission: {str(contestant_err)}', verdict_file)
    report_good_answer()
