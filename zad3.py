import math

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_size = len(alphabet)
target_entropy_bits = 256


ent_per_char = math.log2(alphabet_size)
needed_chars = math.ceil(target_entropy_bits / ent_per_char)

print(f"Entropia jednego znaku [a-z]: {ent_per_char:.4f} bitów")
print(f"Aby osiągnąć {target_entropy_bits}-bitową entropię (jak AES-256), potrzeba co najmniej {needed_chars} znaków [a-z].")
print(f"Łączna entropia dla {needed_chars} znaków: {needed_chars * ent_per_char:.2f} bitów")