from lib.template_holder import TemplateHolder

import json


class Compressor(object):
    def __init__(self, template_lines: list):
        self.template_holder = TemplateHolder(template_lines)

    def compress(self, lines):
        """
        :param lines: list of lines, that should be compressed
        :return: list of compressed lines
        """
        result = []
        for line_idx, line in enumerate(lines):
            idx, tokens = self.template_holder.check_sentence(line)
            if idx == -1:
                raise Exception('line does not match to any template')
            result.append(f'{idx},{json.dumps(tokens)}\n')
        return result

    def decompress(self, lines) -> list:
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
