import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_bit_by_index(byte: int, n: int) -> int:
    return int((byte & (1 << n)) / (1 << n))

def get_bits_from_byte(byte: int) -> list[int]:
    bits = []
    for i in range(8)[::-1]:
        bits += [get_bit_by_index(byte, i)]

    return bits

def bits_to_int(bits: list[int]) -> int:
    return sum([bit << i for i, bit in enumerate(bits[::-1])])

def bits_to_char(bits: list[int]) -> str | None:
    if sum(bits) == 0:
        return None

    return chr(bits_to_int(bits))

def keep_writing(writed: int, bits: list[int]) -> bool:
    return writed < len(bits)

def encrypt_password(password: str):
    return base64.urlsafe_b64encode(password.encode('ascii'))