import base64

def generate_subkeys(master_key):
    subkeys = []
    for i in range(16):
        subkey = (master_key << i) & 0xFFFFFFFFFFFFFFFF  
        subkeys.append(subkey)
    return subkeys

S_BOX = [
    0x3, 0xF, 0xE, 0x8,
    0x2, 0x4, 0xC, 0x1,
    0xA, 0x6, 0x9, 0xB,
    0x7, 0xD, 0x0, 0x5
]

def apply_sbox(value):
    return S_BOX[value & 0xF] | (S_BOX[(value >> 4) & 0xF] << 4) | \
           (S_BOX[(value >> 8) & 0xF] << 8) | (S_BOX[(value >> 12) & 0xF] << 12) | \
           (S_BOX[(value >> 16) & 0xF] << 16) | (S_BOX[(value >> 20) & 0xF] << 20) | \
           (S_BOX[(value >> 24) & 0xF] << 24) | (S_BOX[(value >> 28) & 0xF] << 28)

def apply_pbox(value):
    permuted = 0
    for i in range(32):
        permuted |= ((value >> i) & 0x1) << ((i * 2) % 32) | ((value >> (i + 1)) & 0x1) << ((i * 2 + 1) % 32)
    return permuted

def round_function(R, subkey):
    R = apply_sbox(R)
    R = apply_pbox(R)
    return R ^ subkey

def feistel_encrypt(plaintext, master_key):
    L = (plaintext >> 32) & 0xFFFFFFFF
    R = plaintext & 0xFFFFFFFF
    subkeys = generate_subkeys(master_key)
    
    for subkey in subkeys:
        temp = R
        R = round_function(R, subkey)
        R = R ^ L
        L = temp
    
    ciphertext = (L << 32) | R
    return ciphertext

def text_to_bin(text):
    return int.from_bytes(text.encode(), 'big')

def bin_to_base64(bin_value):
    byte_length = (bin_value.bit_length() + 7) // 8
    return base64.b64encode(bin_value.to_bytes(byte_length, 'big')).decode()

def bin_to_hex(bin_value):
    return hex(bin_value)

plaintext = input("Enter plaintext: ")
key = input("Enter key: ")

plaintext_bin = text_to_bin(plaintext)
key_bin = text_to_bin(key)

plaintext_bin = plaintext_bin & 0xFFFFFFFFFFFFFFFF
key_bin = key_bin & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

ciphertext_bin = feistel_encrypt(plaintext_bin, key_bin)

print("ciphertext (binary):", bin(ciphertext_bin))
print("ciphertext (hex):", bin_to_hex(ciphertext_bin))
print("ciphertext (Base64):", bin_to_base64(ciphertext_bin))
