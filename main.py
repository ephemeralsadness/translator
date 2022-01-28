import argparse
import os
import sys
from pathlib import Path

from translator import Translator


def main():
    parser = argparse.ArgumentParser(description='Java to C++ Translator')
    parser.add_argument('file', metavar='file', type=str, help='path to java source code file')
    parser.add_argument('--cpp', default='a.cpp', type=str, help='path to output c++ code file')
    parser.add_argument('--force', help='force writing to existing file', action='store_true')
    parser.add_argument('--debug', help='debug', action='store_true')
    args = parser.parse_args()
    java_file_name = args.file
    cpp_file_name = args.cpp
    force = args.force
    debug = args.debug

    if not os.path.isfile(java_file_name):
        raise Exception('Cannot find file by that path: {}.'.format(java_file_name))
    if (not force) and (os.path.isdir(cpp_file_name) or os.path.isfile(cpp_file_name)):
        raise Exception('There is a file/directory by that path: {}. '
                        'Please select another path.'.format(cpp_file_name))

    with open(java_file_name, 'r') as java_file:
        with open(cpp_file_name, 'w') as cpp_file:
            translator = Translator(os.path.dirname(Path(java_file_name)), debug)
            cpp_source_code = translator.run(java_file.read())
            cpp_file.write(str(cpp_source_code))
            print('Success. Output saved to {}.'.format(cpp_file_name))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # print(e, file=sys.stderr)
        raise

