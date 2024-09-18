import argparse
import os
from gcodeparser import GcodeParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GcodeParser',
        description='Converts a gcode file into an array of Python objects representing each command',
    )

    parser.add_argument(
        'input_file',
        help='Path to the gcode file to be parsed',
    )

    parser.add_argument(
        '-o',
        '--output_file',
        help='Path to the output file where the parsed gcode will be saved. Defaults to stdout.',
        default='-',
    )

    args = parser.parse_args()

    with open(os.path.expanduser(args.input_file), 'r') as f:
        gcode = f.read()
    parsed_gcode = GcodeParser(gcode)
    if args.output_file == '-':
        for line in parsed_gcode.lines:
            print(line)
    else:
        with open(os.path.expanduser(args.output_file), 'w') as f:
            for line in parsed_gcode.lines:
                f.write(str(line) + '\n')
    pass
