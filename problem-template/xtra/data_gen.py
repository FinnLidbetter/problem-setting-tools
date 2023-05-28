#!/usr/bin/python3

import argparse
import random
import sys
from collections import deque
from enum import Enum


class EnumClass(Enum):
    MEMBER = 'member'
    SOMETHING_ELSE = 'string'

    def __str__(self):
        return self.value


N_MIN = 1
N_MAX = 100000
# We will reseed this with the provided seed or a random seed.
RNG = random.Random(0)


def bounded_int(string, val_min, val_max, name='Value'):
    value = int(string)
    if value < val_min or value > val_max:
        raise argparse.ArgumentTypeError(f'{name} must be in range [{val_min}, {val_max}]')
    return value


def bounded_n(string):
    return bounded_int(string, N_MIN, N_MAX, 'n')


def _parse_args():
    parser = argparse.ArgumentParser('')
    # parser.add_argument(
    #     'n', 
    #     type=bounded_n, 
    #     default=DEFAULT_N,
    #     help='The value of n.'
    # )
    # parser.add_argument(
    #     '--enum-class',
    #     type=EnumClass,
    #     choices=list(EnumClass),
    #     default=EnumClass.MEMBER,
    #     help='Some enum.',
    # )
    parser.add_argument(
        '--seed', type=int, default=random.randint(0, 10000),
        help='The random number to seed the random number generator with.'
    )
    parser.add_argument(
        '--test-name', type=str,
        help='The name for the test case. E.g., "025-small-cases" will produce files '
             '025-small-cases.in and 025-small-cases.desc. If no name is specified, '
             'output will be printed to stdout.'
    )
    return parser.parse_args()


def _validate_with_context(args):
    """Function for any validation that involves more than one argument."""
    # if args.val_min > args.val_max:
    #     raise ValueError('Something useful.')


def generate_output_lines(args):
    """Function to generate a list of output lines."""



def main():
    global RNG
    args = _parse_args()
    _validate_with_context(args)
    RNG = random.Random(args.seed)

    output_lines = generate_output_lines(args)

    output = '\n'.join(output_lines) + '\n'
    command = ' '.join(sys.argv)
    if '--seed' not in sys.argv:
        command += f' --seed {args.seed}'
    if args.test_name is not None:
        test_input_file_name = args.test_name + '.in'
        test_desc_file_name = args.test_name + '.desc'
        with open(test_input_file_name, 'w') as test_input_file:
            test_input_file.write(output)
        with open(test_desc_file_name, 'w') as test_desc_file:
            test_desc_file.write(f'Produced by:\n\t{command}\n')
    else:
        sys.stdout.write(output)


if __name__ == '__main__':
    main()
