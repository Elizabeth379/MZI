import os
import numpy as np
import base64

input_file_path = "input.txt"
output_file_path = "output.txt"
decrypt_file_path = "decrypt.txt"

if not os.path.exists(input_file_path):
    print(f"Input file '{input_file_path}' not found.")
else:
    with open(input_file_path, "r", encoding="utf-8") as file:
        original_message = file.read()
    print("Original message:\n" + original_message)

    def generate_random_matrix(rows, columns):
        return np.random.randint(2, size=(rows, columns), dtype=np.uint8)

    def encrypt(message, generator_matrix):
        message_bytes = message.encode('utf-8')
        encrypted_bytes = bytearray(len(message_bytes))
        rows, columns = generator_matrix.shape

        for i in range(len(message_bytes)):
            encrypted_bytes[i] = message_bytes[i] ^ generator_matrix[i % rows, i % columns]

        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(encrypted_message, generator_matrix):
        encrypted_bytes = base64.b64decode(encrypted_message)
        decrypted_bytes = bytearray(len(encrypted_bytes))
        rows, columns = generator_matrix.shape

        for i in range(len(encrypted_bytes)):
            decrypted_bytes[i] = encrypted_bytes[i] ^ generator_matrix[i % rows, i % columns]

        return decrypted_bytes.decode('utf-8')

    # Размеры матрицы
    n = 512
    k = 256
    generator_matrix = generate_random_matrix(k, n)

    encrypted_message = encrypt(original_message, generator_matrix)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(encrypted_message)
    print(f"\nEncrypted message written to '{output_file_path}'")

    decrypted_message = decrypt(encrypted_message, generator_matrix)

    with open(decrypt_file_path, "w", encoding="utf-8") as file:
        file.write(decrypted_message)
    print(f"\nDecrypted message written to '{decrypt_file_path}'")
