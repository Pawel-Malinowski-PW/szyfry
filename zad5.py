import hashlib
import random
import string

def random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

hash_dict = {}
attempts = 0

while True:
    pwd = random_password()
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()[:6]
    if md5_hash in hash_dict and hash_dict[md5_hash] != pwd:
        print(f"Hasło 1: {hash_dict[md5_hash]}")
        print(f"Hasło 2: {pwd}")
        print(f"Pierwsze 6 znaków MD5: {md5_hash}")
        break
    hash_dict[md5_hash] = pwd
    attempts += 1