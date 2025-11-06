import hashlib
import random
import string
import math

def random_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

hash_dict = {}
attempts = 0
N = 16**6
exact = math.ceil(math.sqrt(2 * N * math.log(2)))
print(f"Teoretycznie: {exact} prób to 50% szans na kolizję.")


while True:
    attempts += 1
    pwd = random_password()
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()[:6]
    
    if md5_hash in hash_dict and hash_dict[md5_hash] != pwd:
        print(f"Kolizja znaleziona po {attempts} próbach.")
        print(f"Hasło 1: {hash_dict[md5_hash]}")
        print(f"Hasło 2: {pwd}")
        print(f"Pierwsze 6 znaków MD5: {md5_hash}")
        break
    
    hash_dict[md5_hash] = pwd

print("\n" + "="*50)
print("EKSPERYMENT - 200 PRÓB Z LISTAMI 4823 HASEŁ")
print("="*50)

collisions_found = 0
no_collisions = 0

for experiment in range(200):
    passwords_list = []
    md5_table = {}
    collision_found = False
    
    for i in range(exact):
        pwd = random_password()
        md5_hash = hashlib.md5(pwd.encode()).hexdigest()[:6]
        passwords_list.append((pwd, md5_hash))
    
    for i, (pwd, md5_hash) in enumerate(passwords_list):
        if md5_hash in md5_table:
            collision_found = True
            break
        md5_table[md5_hash] = (pwd, i)
    
    if collision_found:
        collisions_found += 1
    else:
        no_collisions += 1
print(f"Kolizje znalezione: {collisions_found}/200 ({collisions_found/200*100:.2f}%)")

