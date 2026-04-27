from .srandom import SimpleRNG
from .sformat import encode, decode   

def encrypt(value, key=None, second=None):
    """加密"""
    random_key = False
    if key is None:
        key = SimpleRNG().uuid()[:8]
        random_key = True
    IV = SimpleRNG().uuid().replace("-", "")
    real_key = int(encode(key+IV))
    IV_int = int(encode(IV))
    moduli = second
    if (not hasattr(moduli, "__iter__")) or (not all(isinstance(i, int) for i in moduli)) or len(moduli) == 0:
        moduli = SimpleRNG().my_hash(str(moduli))
    value = int(encode(value)) * real_key * 0x9e3779b97f4a7c15
    hash_list = moduli
    keys = []
    hash_value = real_key

    for i in range(4):
        hash_value = SimpleRNG().my_hash(hash_value, hash_list)
        hash_list = [i for i in hash_value if not i == 0]
        if hasattr(hash_value, '__iter__') and not isinstance(hash_value, (str, int)):
            hash_value = int(''.join(str(h) for h in hash_value))
        keys.append(real_key ^ (hash_value << 1))
        
    for i in range(100000):
        keys[i%4] = (keys[(i-1)%4] ^ (keys[(i-2)%4] + keys[(i-3)%4])) % 2**256
        
    if random_key:
        return (keys[0] * value) ^ keys[1] ^ keys[2] ^ keys[3], decode(str(real_key)), IV
    else:
        return (keys[0] * value) ^ keys[1] ^ keys[2] ^ keys[3], IV

def decrypt(cipher, key, IV, second=None):
    """解密"""
    moduli = second
    if (not hasattr(moduli, "__iter__")) or (not all(isinstance(i, int) for i in moduli)) or len(moduli) == 0:
        moduli = SimpleRNG().my_hash(str(moduli))
    hash_list = moduli

    real_key = int(encode(key+IV))
    keys = []
    hash_value = real_key
    
    for i in range(4):
        hash_value = SimpleRNG().my_hash(hash_value, hash_list)
        hash_list = [i for i in hash_value if not i == 0]
        if hasattr(hash_value, '__iter__') and not isinstance(hash_value, (str, int)):
            hash_value = int(''.join(str(h) for h in hash_value))
        keys.append(real_key ^ (hash_value << 1))
    
    for i in range(100000):
        keys[i%4] = (keys[(i-1)%4] ^ (keys[(i-2)%4] + keys[(i-3)%4])) % 2**256
    
    temp = cipher ^ keys[1] ^ keys[2] ^ keys[3]
    
    if temp % keys[0] != 0:
        raise ValueError("密文被篡改或密钥错误")
    
    value_int = temp // keys[0]
    value_int //= real_key
    value_int //= 0x9e3779b97f4a7c15

    return decode(str(value_int))

