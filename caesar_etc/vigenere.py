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

    if operation_type == 'decrypt':
        new_char_index = (char_index + key_index) % 26

    elif operation_type == 'encrypt':
        new_char_index = (char_index - key_index) % 26

    else:
        raise(Exception('Что то пошло не так'))

    new_char = alphabet[new_char_index]
    return new_char


def match_keyword(input_len, keyword):
    keyword_len = len(keyword)

    if input_len > keyword_len:
        difference = input_len - keyword_len

        number_of_repeats = difference // keyword_len + 1
        additional_part = input_len - keyword_len * number_of_repeats

        keyword = keyword * number_of_repeats + keyword[:additional_part]

    return keyword


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = list()

    keyword = match_keyword(len(plaintext), keyword)

    for original_char, keyword_char in zip(plaintext, keyword):
        new_char = _crypto_char(original_char, keyword_char, 'decrypt')
        ciphertext.append(new_char)

    return "".join(ciphertext)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = list()

    keyword = match_keyword(len(ciphertext), keyword)

    for original_char, keyword_char in zip(ciphertext, keyword):
        new_char = _crypto_char(original_char, keyword_char, 'encrypt')
        plaintext.append(new_char)

    return "".join(plaintext)
