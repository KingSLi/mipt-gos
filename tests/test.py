from lib.compress_lib import Compressor
import json
import os


def main():
    RAW_FILE = 'raw_messages.txt'
    COMPRESSED_FILE = 'compressed_messages.txt'
    TEMPLATES_FILE = 'templates.json'

    with open(TEMPLATES_FILE, 'r') as f:
        templates_list = json.load(f)
    compressor = Compressor(templates_list)

    with open(RAW_FILE, 'r') as f:
        raw_lines = f.readlines()

    compressed_lines = compressor.compress(raw_lines)
    decompressed_lines = compressor.decompress(compressed_lines)

    with open(COMPRESSED_FILE, 'w') as f:
        f.writelines(compressed_lines)

    assert(all(i == j for i, j in zip(raw_lines, decompressed_lines)))

    print("Original file: '{}' - {} bytes".format(RAW_FILE, os.path.getsize(RAW_FILE)))
    print("Compressed file: '{}' - {} bytes".format(COMPRESSED_FILE, os.path.getsize(COMPRESSED_FILE)))


if __name__ == '__main__':
    main()
