import os
from haffman import *


class CoderDecoder:

    def __init__(self):
        self.signature = 'botik'
        self.version = '0002'
        self.algorithms = '100000'
        self.size = '0000'
        self.filename = 'test'

    def get_header(self, filename):
        name = filename.split('.')[0]
        hex_signature = self.signature.encode().hex()
        hex_filename = name.encode().hex()
        hex_size = str(os.stat(filename).st_size).encode().hex()

        return hex_signature + self.version + self.algorithms + hex_size + hex_filename

    def code(self, filename):
        hex_header = self.get_header(filename)
        version = hex_header[10:14]
        algorithm = hex_header[14:20]
        if version == '0002' and algorithm == '100000':
            coding_content_file = run(filename).encode().hex()
        else:
            try:
                with open(filename, 'rb') as file:
                    coding_content_file = file.read().hex()

            except IOError:
                print('Невозможно открыть файл')

        with open(f'{filename}.{self.signature}', 'wb') as file:
            result = hex_header + coding_content_file
            file.write(bytes.fromhex(result))

    def decode(self, filename):
        try:
            with open(filename, 'rb') as file:
                content = file.read().hex()

            hex_signature = self.signature.encode().hex()

            if content.startswith(hex_signature):
                name = '.'.join(filename.split('.')[0:-1])  # fullname first file
                file_extension = filename.split('.')[-2]
                # full_name = name + '.' + file_extension
                without_header = bytes.fromhex(content[len(self.get_header(name)):])
                without_header = bytes.decode(without_header, encoding='utf-8')
                print(f'Длина сжатых данных: {len(without_header)}')
                version = content[len(hex_signature):14]
                algorithm = content[14:20]
                if version == '0002' and algorithm == '100000':
                    with open('codes.txt', 'rb') as inp:
                        codes = pickle.load(inp)
                    print(f'Коды символов:\n{codes}')
                    decoding_content = decoding(without_header, codes)
                else:
                    decoding_content = without_header

                with open(f'test.{file_extension}', 'w') as file:
                    file.write(decoding_content)

            else:
                print('Сигнатура не совпадает')

        except IOError:
            print('Невозможно открыть файл')
