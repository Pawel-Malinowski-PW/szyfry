import requests
from passlib.hash import md5_crypt, sha256_crypt, argon2
import string
import base64
import time

hashes = [
    "$1$k8nhEGc9$MwWuWMnHqzGdszCwI98RZ0",
    "$5$rounds=10000$ujmXZ4IqnXl.Bplf$4lcwpQwc.kZFIuCrV8Mgg8bP.Mv.jxx9NitjrqQPK8/",
    "$argon2id$v=19$m=65536,t=3,p=4$GWMMQYgxJmQshdB6L0UIgQ$+glO5pBsNQ6Fb80yakwkzUfSXdX9nQM0ygF2ZNJ5DwI",
    "$1$o8ZWp.W5$FIkSXN.lufeIWvllfQW9l1"
]

# Pobierz listę haseł
url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
passwords = requests.get(url).text.splitlines()

def crack_md5_crypt(hash_value, passwords):
    salt = hash_value.split('$')[2]
    for i, pwd in enumerate(passwords):
        if i % 100 == 0:
            print(f"MD5-Crypt: sprawdzono {i}/{len(passwords)} haseł", end='\r')
        if md5_crypt.hash(pwd, salt=salt) == hash_value:
            print(f"\nZnaleziono po {i+1} próbach")
            return pwd
    print(f"\nMD5-Crypt: sprawdzono wszystkie {len(passwords)} haseł")
    return None

def crack_sha256_crypt(hash_value, passwords):
    salt = hash_value.split('$')[3]
    rounds = int(hash_value.split('$')[2].split('=')[1])
    for i, pwd in enumerate(passwords):
        if i % 100 == 0:
            print(f"SHA256-Crypt: sprawdzono {i}/{len(passwords)} haseł", end='\r')
        if sha256_crypt.hash(pwd, salt=salt, rounds=rounds) == hash_value:
            print(f"\nZnaleziono po {i+1} próbach!")
            return pwd
    print(f"\nSHA256-Crypt: sprawdzono wszystkie {len(passwords)} haseł")
    return None

def crack_argon2id(hash_value, passwords):
    parts = hash_value.split('$')
    params = parts[3]
    salt_b64 = parts[4]

    memory = time_cost = parallelism = None
    for kv in params.split(','):
        k, v = kv.split('=')
        if k == 'm': memory = int(v)
        elif k == 't': time_cost = int(v)
        elif k == 'p': parallelism = int(v)

    salt_bytes = safe_b64decode(salt_b64)
    
    for i, pwd in enumerate(passwords):
        if i % 50 == 0:
            print(f"Argon2id: sprawdzono {i}/{len(passwords)} haseł", end='\r')
        h = argon2.using(type='id', memory_cost=memory, time_cost=time_cost, 
                        parallelism=parallelism, salt=salt_bytes).hash(pwd)
        if h == hash_value:
            print(f"\nZnaleziono po {i+1} próbach!")
            return pwd
    print(f"\nArgon2id: sprawdzono wszystkie {len(passwords)} haseł")
    return None

def crack_md5_crypt_pepper(hash_value, passwords):
    salt = hash_value.split('$')[2]
    total_attempts = 0
    
    for i, pwd in enumerate(passwords):
        for j, pepper in enumerate(string.ascii_lowercase):
            total_attempts += 1
            if total_attempts % 100 == 0:
                print(f"MD5-Pepper: sprawdzono {total_attempts} kombinacji (hasło {i+1}, pieprz {pepper})", end='\r')
            candidate = pwd + pepper
            if md5_crypt.hash(candidate, salt=salt) == hash_value:
                print(f"\nZnaleziono po {total_attempts} próbach!")
                return candidate
    print(f"\nMD5-Pepper: sprawdzono wszystkie {total_attempts} kombinacji")
    return None

def safe_b64decode(s):
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return base64.b64decode(s)

print("Hash 1 (MD5-Crypt):", crack_md5_crypt(hashes[0], passwords))
print("Hash 2 (SHA256-Crypt):", crack_sha256_crypt(hashes[1], passwords))
print("Hash 4 (MD5-Crypt + pepper):", crack_md5_crypt_pepper(hashes[3], passwords))
print("Hash 3 (Argon2id):", crack_argon2id(hashes[2], passwords))
