#********************************************************
# Module Name   : AES GOlden Model 
# Author        : Inc
# Revision      : V1
# DoR           : Aug 2021
# History       :
#********************************************************

from binascii import hexlify,unhexlify
from aes import AES
import random

class AES_Golden_Model:
    def __init__(self,key_data): # key_data should be in bytes form
        self.key_data   = int.from_bytes(key_data,byteorder='big')
        self.aes_obj    = AES (self.key_data)

    def get_cipher_data (self,plain_data): # plain data should be in bytes form
         plain_data_int = int.from_bytes(plain_data,byteorder='big')
         cipher_data    = self.aes_obj.encrypt(plain_data_int) # int form
         c_data_in_bytes = cipher_data[0].to_bytes(16,byteorder='big')
         #print (cipher_data)
         return c_data_in_bytes


    def get_xor_cipher_data (self):
        expected =[]
        for i in range(16):
            expected.append(self.key_data[i] ^ self.plain_data[i])
        expected = bytes(expected)
        print (f"[+] Computed Cipher Data of Golden AES model is: {hexlify(expected).decode().upper()}")
        return expected


if __name__ == "__main__":
    print ("AES Golden Model has started....")
    key_val  = [00,17,34,51,68,85,102,119,136,153,170,187,204,221,238,255]
    data_val  = [00,17,34,51,68,85,102,119,136,153,170,187,204,221,238,255]

    obj1 = AES_Golden_Model(bytes(key_val))
    c1     = obj1.get_cipher_data (bytes(data_val))
    print (c1)
    print (hexlify(c1).decode().upper())
