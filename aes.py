from cryptography.fernet import Fernet

def encrypter(key, plaintext: str):
    fernet = Fernet(key)
    return fernet.encrypt(plaintext.encode())

def decrypter(key, ciphertext: str):
    fernet = Fernet(key)
    return fernet.decrypt(ciphertext).decode()

def generate_key():
    key = Fernet.generate_key()
    keyFile = open("key.txt","w+")
    keyFile.write(key.decode())
    keyFile.close()
    return key

def upload_key(keyFilePath):
    keyFile = open(keyFilePath,"rb")
    key = keyFile.read()
    keyFile.close()
    return key