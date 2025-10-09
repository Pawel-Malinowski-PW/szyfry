import itertools
import math

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    # KSA
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    # PRGA
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

def entropy(data):
    if not data:
        return 0
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    ent = 0
    for count in freq.values():
        p = count / len(data)
        ent -= p * math.log2(p)
    return ent

def brute_force_rc4(filename):
    with open(filename, "rb") as f:
        ciphertext = f.read()
    min_entropy = float('inf')
    likely_key = None
    likely_plain = None
    for idx, key_tuple in enumerate(itertools.product(range(ord('a'), ord('z')+1), repeat=3)):
        if idx % 1000 == 0:
            print(f"Przetworzono {idx} kluczy...")
        key = bytes(key_tuple)
        plain = rc4(key, ciphertext)
        ent = entropy(plain)
        # Entropia tekstu jawnego (język naturalny) powinna być niższa niż losowego ciągu bajtów
        if ent < min_entropy:
            min_entropy = ent
            likely_key = key
            likely_plain = plain
    print(f"Najbardziej prawdopodobny klucz dla {filename}: {likely_key.decode('ascii')}")
    print(f"Entropia: {min_entropy:.3f}")
    print("Fragment odszyfrowanego tekstu:", likely_plain[:200])

# Atak na oba pliki
brute_force_rc4("crypto.rc4")
brute_force_rc4("crypto2.rc4")