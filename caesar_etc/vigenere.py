import string


def _crypto_char(char, key, operation_type):
    lower_alphabet = string.ascii_lowercase
    upper_alphabet = string.ascii_uppercase

    if char.islower():
        alphabet = lower_alphabet
        key = key.lower()
    else:
        alphabet = upper_alphabet
        key = key.upper()

    if char not in alphabet:
        return char

    char_index = alphabet.index(char)
    key_index = alphabet.index(key)

    if operation_type == 'encrypt':
        new_char_index = (char_index + key_index) % 26

    elif operation_type == 'decrypt':
        new_char_index = (char_index - key_index) % 26

    else:
        raise(Exception('Что то пошло не так'))

    new_char = alphabet[new_char_index]
    return new_char


def correct_keyword(input_len, keyword):
    keyword_len = len(keyword)

    if input_len > keyword_len:
        difference = input_len - keyword_len

        number_of_repeats = difference // keyword_len + 1
        additional_part = input_len - keyword_len * number_of_repeats

        keyword = keyword * number_of_repeats + keyword[:additional_part]

    return keyword


def cycle(text, keyword, operation_type):
    new_text_array = list()
    keyword = correct_keyword(len(text), keyword)

    for original_char, keyword_char in zip(text, keyword):
        new_char = _crypto_char(original_char, keyword_char, operation_type)
        new_text_array.append(new_char)

    return ''.join(new_text_array)


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    return cycle(plaintext, keyword=keyword, operation_type='encrypt')


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    return cycle(ciphertext, keyword=keyword, operation_type='decrypt')
