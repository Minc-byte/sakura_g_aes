#---------------------------------------------------------
# Module Name   : DataGenerator
# Designer      : Inc
# Ver           : v1
# History       :
#
#-------------------------------------------------------
import random
from binascii import hexlify,unhexlify
import sys

l1 = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']


class DataGenerator():
    def __init__(self,no_of_nibbles):
        NO_OF_BYTES = no_of_nibbles * 2
        self.bytes_data = ''
        for item in [random.choice(l1) for x in range(NO_OF_BYTES)]:
          self.bytes_data = self.bytes_data+item
          
    def get_data (self):
        return unhexlify(self.bytes_data)


if __name__ == "__main__":
    obj_1 = DataGenerator(8);
    tx_stream= obj_1.get_data()
    print (tx_stream)
