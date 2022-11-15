# сжатие строки без контекста (алгоритм RLE наивный)

def code_rle(message):
    encoded_string = ""
    i = 0
    while (i <= len(message) - 1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message) - 1):
            # if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1
            if (message[j] == message[j + 1]):
                count = count + 1
                j = j + 1
            else:
                break
        '''the count and the character is concatenated to the encoded string'''
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string


def decode_rle(our_message):
    decoded_message = ""
    i = 0
    j = 0

    # splitting the encoded message into respective counts
    while (i <= len(our_message) - 1):
        flag = False
        while our_message[i + 1].isdigit():
            i = i + 1
            flag = True
        if flag:
            run_count = int(our_message[:i + 1])
        else:
            run_count = int(our_message[i])
        run_word = our_message[i + 1]
        # displaying the character multiple times specified by the count
        for j in range(run_count):
            # concatenated with the decoded message
            decoded_message = decoded_message + run_word
        i = i + 2
    print(f'Decode string: [{decoded_message}]')
    return decoded_message


def run(filename):
    try:
        with open(filename, 'r') as file:
            content_file = file.read()
            print(f'Длина исходного файла: {len(content_file)}')
    except IOError:
        print('Невозможно открыть файл')

    encoded_message = code_rle(content_file)
    print("Original string: [" + content_file + "]")
    print("Encoded string: [" + encoded_message + "]")

    return encoded_message
