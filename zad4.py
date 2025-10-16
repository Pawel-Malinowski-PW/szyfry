from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import string

def brute_force_bmp_ecb(filename):
    with open(filename, "rb") as f:
        ciphertext = f.read()
        padded_plaintext = pad(ciphertext, 16)
    test_bytes = ciphertext[:16]

    for char in string.ascii_lowercase + string.digits:
        password = char * 16
        key = password.encode("utf-8")
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(test_bytes)
        if decrypted[:2] == b'BM':
            print(f"Znaleziono hasło: {password}")
            full_decrypted = cipher.decrypt(padded_plaintext[:len(padded_plaintext)])
            full_decrypted = unpad(full_decrypted, 16)
            with open("security_ECB_decrypted.bmp", "wb") as out:
                out.write(full_decrypted)
            print("Plik odszyfrowany zapisano jako security_ECB_decrypted.bmp")
            return
    print("Nie znaleziono poprawnego hasła.")

brute_force_bmp_ecb("security_ECB_encrypted.bmp")