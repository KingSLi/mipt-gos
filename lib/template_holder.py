import json


class TemplateHolder(object):

    def __init__(self, template_list, placeholder='{}'):
        self._PLACEHOLDER = placeholder
        self._ENDPOINT = '__end__'
        self._trie = {}
        self._id_to_template = template_list

        for idx, template in enumerate(template_list):
            self._trie_insert(template, idx)

    # public
    def get_template_by_id(self, id: int) -> str:
        if id < 0 or id >= len(self._id_to_template):
            raise Exception('Invalid id of templates')
        return self._id_to_template[id]

    def check_sentence(self, sentence: str) -> (int, list):
        tokens = []
        cur_node = self._trie
        for word in sentence.split(' '):
            word = word.strip()
            if len(word) == 0:
                continue
            if word not in cur_node:
                if self._PLACEHOLDER in cur_node:
                    tokens.append(word)
                    cur_node = cur_node[self._PLACEHOLDER]
                    continue
                else:
                    return -1, []
            cur_node = cur_node[word]
        return cur_node.get(self._ENDPOINT, -1), tokens

    # private
    def _trie_insert(self, template: str, id: int):
        current_dict = self._trie
        for word in template.split(' '):
            word = word.strip()
            if len(word) == 0:
                continue
            current_dict = current_dict.setdefault(word, {})
        current_dict[self._ENDPOINT] = id
