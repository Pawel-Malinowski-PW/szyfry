import collections

def caesar_encrypt(text, shift, alphabet):
    result = ""
    for char in text:
        if char in alphabet:
            idx = alphabet.index(char)
            result += alphabet[(idx + shift) % len(alphabet)]
        else:
            result += char
    return result

def caesar_decrypt(text, shift, alphabet):
    return caesar_encrypt(text, -shift, alphabet)

def letter_freq(text, alphabet):
    counter = collections.Counter([c for c in text if c in alphabet])
    total = sum(counter.values())
    freq = {}
    for letter in alphabet:
        freq[letter] = (counter[letter] / total * 100) if total > 0 else 0
    return freq

def chi_squared_stat(obs_freq, exp_freq, alphabet):
    chi2 = 0
    for letter in alphabet:
        expected = exp_freq.get(letter, 0)
        observed = obs_freq.get(letter, 0)
        if expected > 0:
            chi2 += ((observed - expected) ** 2) / expected
    return chi2

def break_caesar_chi2(ciphertext, alphabet, exp_freq):
    min_chi2 = float('inf')
    likely_shift = 0
    for shift in range(len(alphabet)):
        decrypted = caesar_decrypt(ciphertext, shift, alphabet)
        obs_freq = letter_freq(decrypted, alphabet)
        chi2 = chi_squared_stat(obs_freq, exp_freq, alphabet)
        if chi2 < min_chi2:
            min_chi2 = chi2
            likely_shift = shift
    return likely_shift

# Alfabet dla każdego języka
alphabet_pl = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
alphabet_en = "abcdefghijklmnopqrstuvwxyz"
alphabet_it = "abcdefghijklmnopqrstuvwxyz"

# POLSKI (wg NKJP 2012)
freq_table_pl = {
    'a': 8.965, 'ą': 1.021, 'b': 1.482, 'c': 3.988, 'ć': 0.448, 'd': 3.293, 'e': 7.921,
    'ę': 1.131, 'f': 0.312, 'g': 1.377, 'h': 1.072, 'i': 8.286, 'j': 2.343, 'k': 3.411,
    'l': 2.136, 'ł': 1.746, 'm': 2.911, 'n': 5.600, 'ń': 0.185, 'o': 7.590, 'ó': 0.823,
    'p': 3.101, 'q': 0.003, 'r': 4.571, 's': 4.263, 'ś': 0.683, 't': 3.966, 'u': 2.347,
    'v': 0.034, 'w': 4.549, 'x': 0.019, 'y': 3.857, 'z': 5.620, 'ź': 0.061, 'ż': 0.885
}

# ANGIELSKI (wg Wikipedia)
freq_table_en = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015,
    'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749,
    'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758,
    'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
}

# WŁOSKI (wg Wikipedia)
freq_table_it = {
    'a': 11.745, 'b': 0.927, 'c': 4.501, 'd': 3.736, 'e': 11.792, 'f': 1.153, 'g': 1.644,
    'h': 0.636, 'i': 10.143, 'j': 0.011, 'k': 0.009, 'l': 6.510, 'm': 2.512, 'n': 6.883,
    'o': 9.832, 'p': 3.056, 'q': 0.505, 'r': 6.367, 's': 4.981, 't': 5.623, 'u': 3.011,
    'v': 2.097, 'w': 0.033, 'x': 0.003, 'y': 0.020, 'z': 1.181
}

def read_file(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read().strip()

def write_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

# Wczytaj teksty z plików
plain_pl = read_file("polski.txt")
plain_en = read_file("ang.txt")
plain_it = read_file("wloski.txt")

# Szyfruj teksty (dowolne przesunięcia, np. 7, 3, 10)
shift_pl = 7
shift_en = 3
shift_it = 10

cipher_pl = caesar_encrypt(plain_pl, shift_pl, alphabet_pl)
cipher_en = caesar_encrypt(plain_en, shift_en, alphabet_en)
cipher_it = caesar_encrypt(plain_it, shift_it, alphabet_it)

# Zapisz zaszyfrowane teksty do plików
write_file("zaszyfrowany_pl.txt", cipher_pl)
write_file("zaszyfrowany_en.txt", cipher_en)
write_file("zaszyfrowany_it.txt", cipher_it)

print("Zaszyfrowane teksty zapisane do plików.")

# Wczytaj zaszyfrowane teksty z plików
cipher_pl = read_file("zaszyfrowany_pl.txt")
cipher_en = read_file("zaszyfrowany_en.txt")
cipher_it = read_file("zaszyfrowany_it.txt")

print("\nZaszyfrowane:")
print("PL:", cipher_pl)
print("EN:", cipher_en)
print("IT:", cipher_it)

# Łamanie szyfru (analiza chi-kwadrat)
found_shift_pl = break_caesar_chi2(cipher_pl, alphabet_pl, freq_table_pl)
found_shift_en = break_caesar_chi2(cipher_en, alphabet_en, freq_table_en)
found_shift_it = break_caesar_chi2(cipher_it, alphabet_it, freq_table_it)

print("\nOdszyfrowane (złamane klucze):")
print("PL:", caesar_decrypt(cipher_pl, found_shift_pl, alphabet_pl))
print("EN:", caesar_decrypt(cipher_en, found_shift_en, alphabet_en))
print("IT:", caesar_decrypt(cipher_it, found_shift_it, alphabet_it))

print("\nOdgadnięte przesunięcia:")
print("PL:", found_shift_pl)
print("EN:", found_shift_en)
print("IT:", found_shift_it)