import argparse
import json

from lib.compress_lib import Compressor


def parse_args():
    sub_parser = argparse.ArgumentParser()
    sub_parser.add_argument('--mode', required=True, choices=['compress', 'decompress'])
    sub_parser.add_argument('--input_file', required=True)
    sub_parser.add_argument('--output_file', required=True)
    sub_parser.add_argument('--templates', default='templates.json')
    return sub_parser.parse_args()


def main():
    args = parse_args()

    with open(args.templates, 'r') as f:
        templates_list = json.load(f)
    compressor = Compressor(templates_list)

    with open(args.input_file, 'r') as f:
        lines = f.readlines()

    if args.mode == 'compress':
        result = compressor.compress(lines)
    elif args.mode == 'decompress':
        result = compressor.decompress(lines)
    else:
        raise Exception('Invalid mode')

    with open(args.output_file, 'w') as f:
        f.writelines(result)


if __name__ == '__main__':
    main()
