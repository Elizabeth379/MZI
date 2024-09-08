import os


# выполняет преобразование на основе предыдущего зашифрованного блока - XOR с ключом
def apply_F_theta(prev_Y, key):
    return prev_Y ^ int(key, 2)


# выборка первых Xi_length бит из Z
def mask_L_Xi(value, bit_length):
    mask = (1 << bit_length) - 1  # Генерация маски для битовой длины, гарантирует, что количество бит соответствует длине текущего блока текста.
    return value & mask


def encryption_algorithm(input_path, output_path, key, sync_pos):
    if not os.path.isfile(input_path):
        print(f"Файл '{input_path}' не найден. Операция шифрования невозможна.")
        return

    # Чтение входного файла как строки и преобразование в список кодов символов (ASCII)
    with open(input_path, 'r', encoding='utf-8') as infile:
        plaintext = infile.read()
        blocks = [ord(char) for char in plaintext]  # Символы переводим в их ASCII-коды

    # Начальное значение Y0 (синхропосылка)
    prev_Y = int(sync_pos, 2)

    encrypted = []
    block_length = max(len(bin(block)) - 2 for block in blocks)  # Определяем длину блока (в битах)

    for block in blocks:
        # Преобразование через F_theta
        gamma = apply_F_theta(prev_Y, key)
        # Применение маски к блоку
        masked_gamma = mask_L_Xi(gamma, block_length)
        # XOR между текущим блоком и гаммой
        encrypted_block = block ^ masked_gamma
        encrypted.append(encrypted_block)
        # Обновление предыдущего зашифрованного блока для следующего шага
        prev_Y = encrypted_block

    # Записываем зашифрованные значения в файл, преобразуя обратно в символы
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(''.join(chr(b) for b in encrypted))

    print(f"Шифрование завершено. Результат записан в файл '{output_path}'.")


def decryption_algorithm(input_path, output_path, key, sync_pos):
    if not os.path.isfile(input_path):
        print(f"Файл '{input_path}' не найден. Операция дешифрования невозможна.")
        return

    # Чтение входного файла и преобразование символов обратно в ASCII-коды
    with open(input_path, 'r', encoding='utf-8') as infile:
        encrypted = infile.read()
        blocks = [ord(char) for char in encrypted]

    # Начальное значение Y0 (синхропосылка)
    prev_Y = int(sync_pos, 2)

    decrypted = []
    block_length = max(len(bin(block)) - 2 for block in blocks)  # Определяем длину блока

    for block in blocks:
        # Преобразование через F_theta
        gamma = apply_F_theta(prev_Y, key)
        # Применение маски
        masked_gamma = mask_L_Xi(gamma, block_length)
        # XOR между зашифрованным блоком и гаммой
        decrypted_block = block ^ masked_gamma
        decrypted.append(decrypted_block)
        # Обновление предыдущего блока
        prev_Y = block

    # Записываем расшифрованные данные в файл
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(''.join(chr(b) for b in decrypted))

    print(f"Дешифрование завершено. Результат записан в файл '{output_path}'.")


def main():
    operation = input("Введите '1' для шифрования или '2' для дешифрования: ").strip()

    input_filename = 'input.txt'
    encrypted_filename = 'encrypted.txt'
    decrypted_filename = 'decrypted.txt'

    key = '101010'
    sync_pos = '11111111'

    if operation == '1':
        encryption_algorithm(input_filename, encrypted_filename, key, sync_pos)
    elif operation == '2':
        decryption_algorithm(encrypted_filename, decrypted_filename, key, sync_pos)
    else:
        print("Неверный выбор. Введите '1' для шифрования или '2' для дешифрования.")


if __name__ == "__main__":
    main()
