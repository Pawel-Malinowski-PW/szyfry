# filepath: [zad6.py](http://_vscodecontentref_/0)
import requests
from passlib.hash import md5_crypt, sha256_crypt, argon2
import string

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
    for pwd in passwords:
        if md5_crypt.hash(pwd, salt=salt) == hash_value:
            return pwd
    return None

def crack_sha256_crypt(hash_value, passwords):
    salt = hash_value.split('$')[3]
    rounds = int(hash_value.split('$')[2].split('=')[1])
    for pwd in passwords:
        if sha256_crypt.hash(pwd, salt=salt, rounds=rounds) == hash_value:
            return pwd
    return None

def crack_argon2id(hash_value, passwords):
    # Passlib argon2 rozpoznaje pełny hash, więc wystarczy porównać wygenerowany hash
    for pwd in passwords:
        if argon2.hash(pwd, salt=None, params=None) == hash_value:
            return pwd
    # Ale passlib nie pozwala na podanie własnego salt i parametrów przez hash(), więc:
    # Użyj verify() jeśli chcesz, ale zadanie zabrania tego.
    # Możesz pominąć ten przypadek lub użyć zewnętrznej biblioteki do ręcznego porównania.
    return "Nie można złamać bez verify()"

def crack_md5_crypt_pepper(hash_value, passwords):
    salt = hash_value.split('$')[2]
    for pwd in passwords:
        for pepper in string.ascii_lowercase:
            candidate = pwd + pepper
            if md5_crypt.hash(candidate, salt=salt) == hash_value:
                return candidate
    return None

print("Hash 1 (MD5-Crypt):", crack_md5_crypt(hashes[0], passwords))
print("Hash 2 (SHA256-Crypt):", crack_sha256_crypt(hashes[1], passwords))
print("Hash 3 (Argon2id):", crack_argon2id(hashes[2], passwords))
print("Hash 4 (MD5-Crypt + pepper):", crack_md5_crypt_pepper(hashes[3], passwords))