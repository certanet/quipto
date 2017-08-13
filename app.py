import base64
import os
from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2


class Quipto:

    def __init__(self):
        pass

    def pad_data(self, data):
        if len(data) % 16 == 0:
            return data
        databytes = bytearray(data)
        padding_required = 15 - (len(databytes) % 16)
        databytes.extend(b'\x80')
        databytes.extend(b'\x00' * padding_required)
        return bytes(databytes)

    def unpad_data(self, data):
        if not data:
            return data
        data = data.rstrip(b'\x00')
        if data[-1] == 128:
            return data[:-1]
        else:
            return data

    def Encrypt(self, pt, secret):
        secret_enc = secret.encode('utf-8')
        pt_enc = self.pad_data(pt.encode('utf-8'))

        key = PBKDF2(secret_enc, salt).read(32)
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = iv + cipher.encrypt(pt_enc)

        ct_enc = base64.b64encode(ct)
        return ct_enc

    def Decrypt(self, ct, secret):
        secret_enc = secret.encode('utf-8')

        try:
            ct_dec = base64.b64decode(ct.decode())
        except:
            return "ERROR: CT looks invalid"

        key = PBKDF2(secret_enc, salt).read(32)
        iv = ct_dec[:AES.block_size]

        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
        except:
            return "ERROR: Decryption error, check CT"

        pt = cipher.decrypt(ct_dec[AES.block_size:])

        try:
            pt_dec = self.unpad_data(pt).decode('utf-8')
        except:
            return "ERROR: Decryption error, check secret or salt"

        return pt_dec


if __name__ == '__main__':
    if "QUIPTO_SALT" in os.environ:
        print("Stored salt detected!")
        salt = eval(os.environ['QUIPTO_SALT'])
    else:
        print("No salt found, generating salt")
        salt = os.urandom(8)
        os.environ['QUIPTO_SALT'] = str(salt)
        salt = eval(os.environ['QUIPTO_SALT'])
        print("ENV SALT = " + str(salt))

    if "QUIPTO_SECRET" in os.environ:
        print("Stored secret detected!")
        secret = os.environ['QUIPTO_SECRET']
    else:
        print("No secret found...")
        secret = str(getpass("Enter secret: "))

    enigma = Quipto()
    while True:
        go = input("(e)ncrypt / (d)ecrypt / (q)uit?: ")

        if go == "e":
            pt = str(input("Enter PT: "))
            ct = enigma.Encrypt(pt, secret)
            print("CT data is: " + str(ct)[1:])
        elif go == "d":
            ct = str.encode(input("Enter CT: "))
            print(str(enigma.Decrypt(ct, secret)))
        elif go == 'q':
            break
