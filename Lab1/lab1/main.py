import os

# Стандартные S-боксы по ГОСТ 28147-89
S_BOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
]


def f(right_part, key):
    temp = (right_part + key) % (1 << 32)
    result = 0
    for i in range(8):
        s_box_input = (temp >> (4 * i)) & 0b1111
        s_box_output = S_BOX[i][s_box_input]
        result |= s_box_output << (4 * i)
    result = ((result << 11) | (result >> (32 - 11))) % (1 << 32)
    return result


def generate_subkeys(master_key):
    assert len(master_key) == 32
    subkeys = []
    for i in range(8):
        subkey = int.from_bytes(master_key[i * 4:(i + 1) * 4], byteorder='little')
        subkeys.append(subkey)
    return subkeys

#Функция режима шифрования с простой заменой
def encrypt_block(block, subkeys):
    n1 = int.from_bytes(block[:4], byteorder='little')
    n2 = int.from_bytes(block[4:], byteorder='little')
    for i in range(32):
        key = subkeys[i % 8]
        temp = n1
        n1 = n2 ^ f(n1, key)
        n2 = temp
    encrypted_block = n1.to_bytes(4, byteorder='little') + n2.to_bytes(4, byteorder='little')
    return encrypted_block


def gost_ofb_encrypt(plaintext, master_key, iv):
    subkeys = generate_subkeys(master_key)
    output = b''
    gamma = iv
    for i in range(0, len(plaintext), 8):
        gamma = encrypt_block(gamma, subkeys) #Используем шифрование с простой заменой для получения гаммы
        block = plaintext[i:i + 8]
        # Дополнение блока до 8 байт
        if len(block) < 8:
            block += b'\0' * (8 - len(block))
        encrypted_block = bytes(a ^ b for a, b in zip(block, gamma))
        output += encrypted_block
    return output


def gost_ofb_decrypt(ciphertext, master_key, iv, plaintext_len):
    subkeys = generate_subkeys(master_key)
    output = b''
    gamma = iv
    for i in range(0, len(ciphertext), 8):
        gamma = encrypt_block(gamma, subkeys)
        block = ciphertext[i:i + 8]
        decrypted_block = bytes(a ^ b for a, b in zip(block, gamma))
        output += decrypted_block

    # Обрезаем лишние символы, которые были добавлены при дополнении блока
    return output[:plaintext_len]


def load_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def save_file(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)


def main():
    master_key = os.urandom(32)
    iv = os.urandom(8)

    # Загрузка исходного текста
    plaintext = load_file('input.txt')
    plaintext_len = len(plaintext)  # Сохраняем исходную длину текста

    # Шифрование
    ciphertext = gost_ofb_encrypt(plaintext, master_key, iv)
    save_file('encrypted.bin', ciphertext)
    print("Шифрование завершено. Зашифрованные данные сохранены в 'encrypted.bin'.")

    # Дешифрование
    decrypted_text = gost_ofb_decrypt(ciphertext, master_key, iv, plaintext_len)
    save_file('decrypted.txt', decrypted_text)
    print("Дешифрование завершено. Расшифрованные данные сохранены в 'decrypted.txt'.")


if __name__ == '__main__':
    main()
