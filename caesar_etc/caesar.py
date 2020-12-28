import string


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:

    lower_alphabet = string.ascii_lowercase
    upper_alphabet = string.ascii_uppercase
    result = list()

    for char in plaintext:

        if char.islower():
            alphabet = lower_alphabet
        else:
            alphabet = upper_alphabet

        if char not in alphabet:
            result.append(char)
            continue

        char_index = alphabet.index(char)
        new_char_index = (char_index + shift)
        new_char_index %= 26
        new_char = alphabet[new_char_index]

        result.append(new_char)

    ciphertext = "".join(result)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    lower_alphabet = string.ascii_lowercase
    upper_alphabet = string.ascii_uppercase
    result = list()

    for char in ciphertext:
        if char.islower():
            alphabet = lower_alphabet
        else:
            alphabet = upper_alphabet

        if char not in alphabet:
            result.append(char)
            continue

        char_index = alphabet.index(char)
        new_char_index = char_index + (26 - shift)
        new_char_index %= 26
        new_char = alphabet[new_char_index]

        result.append(new_char)

    ciphertext = "".join(result)

    return ciphertext
