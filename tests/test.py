from lib.compress_lib import Compressor
import json
import os


def test1():
    RAW_FILE = 'raw_messages.txt'
    COMPRESSED_FILE = '1compressed_messages.txt'
    TEMPLATES_FILE = 'templates.json'

    with open(TEMPLATES_FILE, 'r') as f:
        templates_list = json.load(f)
    compressor = Compressor(templates_list)

    with open(RAW_FILE, 'r') as f:
        raw_lines = f.readlines()

    compressed_lines = compressor.compress_template(raw_lines)
    decompressed_lines = compressor.decompress_template(compressed_lines)

    with open(COMPRESSED_FILE, 'w') as f:
        f.writelines(compressed_lines)

    assert(all(i == j for i, j in zip(raw_lines, decompressed_lines)))

    print("Original file: '{}' - {} bytes".format(RAW_FILE, os.path.getsize(RAW_FILE)))
    print("Compressed file: '{}' - {} bytes".format(COMPRESSED_FILE, os.path.getsize(COMPRESSED_FILE)))


def test2():
    RAW_FILE = 'raw_messages.txt'
    COMPRESSED_FILE = '2compressed_messages.txt'
    DECOMPRESSED_FILE = '2decompressed_messages.txt'
    TEMPLATES_FILE = 'templates.json'

    with open(TEMPLATES_FILE, 'r') as f:
        templates_list = json.load(f)
    compressor = Compressor(templates_list)

    compressed_lines = compressor.compress(RAW_FILE, COMPRESSED_FILE)
    decompressed_lines = compressor.decompress(COMPRESSED_FILE, DECOMPRESSED_FILE)

    with open(RAW_FILE, 'r') as f1, open(DECOMPRESSED_FILE, 'r') as f2:
        for l1, l2 in zip(f1.readlines(), f2.readlines()):
            assert l1 == l2

    print("Original file: '{}' - {} bytes".format(RAW_FILE, os.path.getsize(RAW_FILE)))
    print("Compressed file: '{}' - {} bytes".format(COMPRESSED_FILE, os.path.getsize(COMPRESSED_FILE)))
    print("DeCompressed file: '{}' - {} bytes".format(DECOMPRESSED_FILE, os.path.getsize(DECOMPRESSED_FILE)))


if __name__ == '__main__':
    print("\nTEST1")
    test1()
    print("\nTEST2")
    test2()
