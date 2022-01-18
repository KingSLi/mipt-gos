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

    if args.mode == 'compress':
        compressor.compress(args.input_file, args.output_file)
    elif args.mode == 'decompress':
        compressor.decompress(args.input_file, args.output_file)
    else:
        raise Exception('Invalid mode')


if __name__ == '__main__':
    main()
