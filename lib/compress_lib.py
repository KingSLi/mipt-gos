from lib.template_holder import TemplateHolder
from lib.LZW import LZWCompressor

import json


class Compressor(object):

    def __init__(self, template_lines: list):
        self.template_holder = TemplateHolder(template_lines)
        self.lzw = LZWCompressor()
        self.TMP_FILE_NAME = 'tmp_file.txt'

    def compress_template(self, lines):
        """
        :param lines: list of lines, that should be compressed
        :return: list of compressed lines
        """
        result = []
        for line_idx, line in enumerate(lines):
            idx, tokens = self.template_holder.check_sentence(line)
            if idx == -1:
                raise Exception('line does not match to any template')
            result.append(f'{idx},{json.dumps(tokens, separators=(",", ":"))}\n')
        return result

    def decompress_template(self, lines) -> list:
        """
        :param lines: list of compressed messages
        :return: list of decompressed messages
        """
        result = []
        for line in lines:
            idx, tokens = line.split(',', maxsplit=1)
            template = self.template_holder.get_template_by_id(int(idx))
            tokens = json.loads(tokens)
            s = template.format(*tokens) + '\n'
            result.append(s)
        return result

    def compress(self, input_file, output_file):
        self.compress_with_files(input_file, self.TMP_FILE_NAME, self.compress_template, False)
        self.compress_with_files(self.TMP_FILE_NAME, output_file, self.lzw.compress, True)

    def decompress(self, input_file, output_file):
        self.compress_with_files(input_file, self.TMP_FILE_NAME, self.lzw.decompress, True)
        self.compress_with_files(self.TMP_FILE_NAME, output_file, self.decompress_template, False)

    def compress_with_files(self, inp, out, func, is_byte):
        with open(inp, 'rb' if is_byte else 'r') as f:
            lines = f.read() if is_byte else f.readlines()
        result = func(lines)
        with open(out, 'wb' if is_byte else 'w') as f:
            if is_byte:
                f.write(result)
            else:
                f.writelines(result)
