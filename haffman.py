# кодирование строки по алгоритму Хаффмана.
from collections import Counter
import pickle


class Node:

    def __init__(self, value, left=None, right=None):
        self.right = right
        self.left = left
        self.value = value


def get_code(root, codes=dict(), code=''):
    if root is None:
        return

    if isinstance(root.value, str):
        codes[root.value] = code
        return codes

    get_code(root.left, codes, code + '0')
    get_code(root.right, codes, code + '1')

    return codes


def get_tree(string):
    string_count = Counter(string)

    if len(string_count) <= 1:
        node = Node(None)

        if len(string_count) == 1:
            node.left = Node([key for key in string_count][0])
            node.right = Node(None)

        string_count = {node: 1}

    while len(string_count) != 1:
        node = Node(None)
        spam = string_count.most_common()[:-3:-1]

        if isinstance(spam[0][0], str):
            node.left = Node(spam[0][0])

        else:
            node.left = spam[0][0]

        if isinstance(spam[1][0], str):
            node.right = Node(spam[1][0])

        else:
            node.right = spam[1][0]

        del string_count[spam[0][0]]
        del string_count[spam[1][0]]
        string_count[node] = spam[0][1] + spam[1][1]

    return [key for key in string_count][0]


def code_haf(string, codes):
    res = ''

    for symbol in string:
        res += codes[symbol]

    return res


def decode_haf(string, codes):
    res = ''
    i = 0

    while i < len(string):
        for code in codes:
            # возвращает наименьший индекс, по которому обнаруживается начало указанной подстроки в исходной
            if string[i:].find(codes[code]) == 0:
                res += code
                i += len(codes[code])

    return res


def run(filename=None, content=None):
    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content_file = file.read()

        except IOError:
            print('Невозможно открыть файл')
    else:
        content_file = content
    tree = get_tree(content_file)
    codes = get_code(tree)

    with open('codes.txt', 'wb') as out:
        pickle.dump(codes, out)

    return code_haf(content_file, codes)
