#-----------------------------------------------------------------
# Module Name   : Sakura AES class
# Author        : Inc
# Revision      : v2
# DoR           : Aug 21
# History       : <FINAL WORKING MODEL>
#                 [v2] Added AES 128 Golden Model
#
#
#-----------------------------------------------------------------
from FTDI_dev   import FTDI_dev
from binascii   import hexlify,unhexlify
import sys
from DataGenerator import DataGenerator
import time
import random
from AES_Golden_Model import AES_Golden_Model
from Logger import Logger


#----------- PRE CONFIGURATION DATA ----------------------#
UNIT_TEST        = False 
SLEEP_TIME       = 3 # time to sleep, should sync with the Oscilloscope
TEST_CASES_CNT   = 1000

class Sakura_AES:
    total_no_of_cases = 0
    pass_tests        = 0
    fail_tests        = 0

    def __init__(self,ftdi_dev_obj):
        self.dev_obj = ftdi_dev_obj

    def key_load(self, key_data):
        #print (f"[+] Key Value:X{hexlify(bytes(key_data)).decode().upper()}")
        #print (f"[+] Key loading is in progress ......")
        self.write_reg (b'\x01\x00',bytes(key_data[0 :2] ))  
        self.write_reg (b'\x01\x02',bytes(key_data[2 :4] ))
        self.write_reg (b'\x01\x04',bytes(key_data[4 :6] ))
        self.write_reg (b'\x01\x06',bytes(key_data[6 :8] ))
        self.write_reg (b'\x01\x08',bytes(key_data[8 :10]))
        self.write_reg (b'\x01\x0a',bytes(key_data[10:12]))
        self.write_reg (b'\x01\x0c',bytes(key_data[12:14]))
        self.write_reg (b'\x01\x0e',bytes(key_data[14:  ]))
        #print (f"[+]  Key load Operation is Done.")
    
    def data_load (self,plain_data):
        #print (f"[+] Data Value: X{hexlify(bytes(plain_data)).decode().upper()}")
        #print (f"[+] Data loading is in progress ......")
        self.write_reg (b'\x01\x40',bytes(plain_data [0 :2 ] ))
        self.write_reg (b'\x01\x42',bytes(plain_data[2 :4 ] ))
        self.write_reg (b'\x01\x44',bytes(plain_data[4 :6 ] ))
        self.write_reg (b'\x01\x46',bytes(plain_data[6 :8 ] ))
        self.write_reg (b'\x01\x48',bytes(plain_data[8 :10] ))
        self.write_reg (b'\x01\x4a',bytes(plain_data[10:12] ))
        self.write_reg (b'\x01\x4c',bytes(plain_data[12:14] ))
        self.write_reg (b'\x01\x4e',bytes(plain_data[14:  ] ))
        #print (f"[+]  Plain Data load Operation is Done.")

    def write_reg (self,addr,data):
        #print (f"[+] Writing Operation is initiating....... ")
        #print (f"[+] Writing Address: X{hexlify(addr).decode().upper()}  with Data: X{hexlify(data).decode().upper()}")
        self.dev_obj.send_data(b'\x01')   # Writing <WRITE OP> Code Config
        self.dev_obj.send_data(addr[0:1]) # Writing Higher Addr Byte
        self.dev_obj.send_data(addr[1:])  # Writing Lower  Addr Byte
        self.dev_obj.send_data(data[0:1]) # Writing Higher Data Byte
        self.dev_obj.send_data(data[1:])  # Writing Lower  Data Byte
        #print (f"[+] Writing Operation is Done.")

    def read_reg (self,addr):
        #print (f"[+] Reading Operation is initiating..... ")
        data_h_byte = b''
        data_l_byte = b''
        #print (f"[+] Reading Address(Hex):X{hexlify(addr).decode().upper()}")
        self.dev_obj.send_data(b'\x00')         # Writing <READ OP> Code Config
        self.dev_obj.send_data(addr[0:1])       # Writing Higher Addr Byte
        self.dev_obj.send_data(addr[1:])        # Writing Lower  Addr Byte
        data_h_byte = self.dev_obj.recv_data(1) # Reading Higher Data Byte
        data_l_byte = self.dev_obj.recv_data(1) # Reading Lower  Data Byte
        #print (f"[+] Read Higher Byte data: X{hexlify(data_h_byte).decode().upper()}")
        #print (f"[+] Read Lower  Byte data: X{hexlify(data_l_byte).decode().upper()}")
        #print (f"[+] Reading Operation is Done.")
        if (data_h_byte == b''):
            print (f"[X] Error: Read Null High Byte ! Terminating...")
            sys.exit(1)
        elif (data_l_byte == b''):
            #print (f"[X] Error: Read Null Low Byte ! Terminating...")
            sys.exit(1)
        return data_h_byte + data_l_byte

    @staticmethod
    def is_bit_set (reg_byte,bit_position):
        if reg_byte == b'':
            print (f"[x] Error in received byte")
            sys.exit(1)

        #print (f"[+] Bit Setting Operation is in progress .....")
        var_1 = reg_byte >> bit_position
        #print (f"[+] Bit Setting Operation is Done.")
        if (var_1 & 1 == 1):
            return True
        else:
            return False

    def recv_cipher_data (self):
        #print (f"[+] Receiving Cipher Data is in progres.....")
        cipher_data = b''
        cipher_data = cipher_data + self.read_reg (b'\x01\x80')
        cipher_data = cipher_data + self.read_reg (b'\x01\x82')
        cipher_data = cipher_data + self.read_reg (b'\x01\x84')
        cipher_data = cipher_data + self.read_reg (b'\x01\x86')
        cipher_data = cipher_data + self.read_reg (b'\x01\x88')
        cipher_data = cipher_data + self.read_reg (b'\x01\x8a')
        cipher_data = cipher_data + self.read_reg (b'\x01\x8c')
        cipher_data = cipher_data + self.read_reg (b'\x01\x8e')
        #print (f"[+] Received Cipher Data: X{hexlify(cipher_data).decode().upper()}")
        #print (f"[+] Receiving Cipher Data is Done.")
        return cipher_data
    
    def key_gen_start (self):
        #print (f"[+] Key gen start is iniating....")
        self.write_reg (b'\x00\x02',b'\x00\x02')
        #print (f"[+] Key gen is initiated.")


    def aes_core_start (self):
        #print (f"[+] AES core start is iniating....")
        self.write_reg (b'\x00\x02',b'\x00\x01')
        #print (f"[+] AES core start is initiated.")

    def is_key_exp_done (self, TIME_OUT_CNT=10):
        #print (f"[+] Checking for Key Expansion Status")
        cnt =0
        chk_data = self.read_reg (b'\x00\x0c')
        while (Sakura_AES.is_bit_set(chk_data[1],4) == False):
            chk_data = self.read_reg (b'\x00\x0c')
            #print (f"[+] Checking Lower Data Byte: {chk_data[1]}")
            cnt = cnt+1
            if (cnt == TIME_OUT_CNT):
                print (f"[-] Time out occured. Check Configuration !!!")
                return False
        #print (f"[+] Key Expansion is Done.")
        return True
            
    def is_data_load_done (self, TIME_OUT_CNT=10):
        #print (f"[+] Checking for Data Loading Status")
        cnt =0
        chk_data = self.read_reg (b'\x00\x0c')
        if chk_data == b'':
            print (f"[X] Error: Read Data Register Error")
            print (f"DBG: {chk_data}")
            sys.exit(1)
        while (Sakura_AES.is_bit_set(chk_data[1],3) == False):
            chk_data = self.read_reg (b'\x00\x0c')
            #print (f"[+] Checking Lower Data Byte: {chk_data[1]}")
            cnt = cnt+1
            if (cnt == TIME_OUT_CNT):
                print (f"[-] Time out occured. Check Configuration. Shutting Down !!!")
                sys.exit(1)
        #print (f"[+] Data Loading is Done.")
        return True

    def is_aes_done (self, TIME_OUT_CNT=10):
        #print (f"[+] Checking for AES core is done....")
        cnt =0
        chk_data = self.read_reg (b'\x00\x0c')
        while (Sakura_AES.is_bit_set(chk_data[1],5) == False):
            chk_data = self.read_reg (b'\x00\x0c')
            #print (f"[+] Checking Lower Data Byte: {chk_data[1]}")
            cnt = cnt+1
            if (cnt == TIME_OUT_CNT):
                print (f"[-] Time out occured. Check Configuration !!!")
                return False
        #print (f"[+] AES Core is Done.")
        return True

    def is_data_match (self,key,data,cipher,log_obj):
        #print (f"[+] Data Match Operation is in progres ....")
        #print (f"key   :X{hexlify(key).decode().upper()}")
        #print (f"data  :X{hexlify(data).decode().upper()}")
        
        # Golden Model of AES
        aes_gold_obj = AES_Golden_Model(bytes(key))
        expected     = aes_gold_obj.get_cipher_data(bytes(data))
      
        log_obj.info (f"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log_obj.info (f"[+] Golden Model Cipher Data:X{hexlify(expected).decode().upper()}")
        log_obj.info (f"[+] cipher Received         :X{hexlify(cipher).decode().upper()}  ")
        log_obj.info (f"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        # comparaison b/w computed expectation and received
        for i in range (16):
            if (expected[i] != cipher [i]):
                print (f"[x] Mismatch is done at {i+1} byte position")
                print (f"[!]Expected Val:X{hex(expected[i])}")
                print (f"[!]Cipher   Val:X{hex(cipher[i])  }")
                return False
        return True

    def results_summary(self,log_obj):
        log_obj.info (f"+======================== SUMMARY ========================+")
        log_obj.info (f"|No of Tests initiated  : {Sakura_AES.total_no_of_cases}   ")
        log_obj.info (f"|No of Pass test cases  : {Sakura_AES.pass_tests}          ")
        log_obj.info (f"|No of Fail test cases  : {Sakura_AES.fail_tests}          ")
        log_obj.info (f"+=========================================================+")


if __name__ == "__main__":
    log_obj = Logger('results.log').get_logger_obj()
    log_obj.info(F"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    log_obj.info(F"|    S     A     K     U     R     A   -  A  E  S   -   S  C  A                       |")
    log_obj.info(F"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    RANDOM_TEST = True  # random test flag for 100 test cases
    # Create FTDI Connection
    ftdi_dev_obj = FTDI_dev (b'FT6AQ0JZA')
    log_obj.info (f"[+] Success: FTDI Device was Started Successfully ")

    # Create AES Object
    aes_obj      = Sakura_AES(ftdi_dev_obj)

    # Load AES Key
    #RANDOM KEY
    key_val= []
    for i in range(16):
        key_val.append(random.randint(0,255))
    #print (f"KEY Val: {bytes(key_val)}")
    #FIXED KEY
    #key_val = b'\x11\x11\x22\x22\x33\x33\x44\x44\x55\x55\x66\x66\x77\x77\x88\x99'

    #--------------------- SESSION_KEY_WORD-----------------------------
    session_key_name = input("Enter session key word: ")
    log_obj.info (f"[+] session key is created: {session_key_name}")

    #********************** KEY FILE ***************************************
    key_file_name = "key_" + session_key_name + ".txt"
    log_obj.info (f"[+] Key file created: {key_file_name}")
    with open (key_file_name,"w") as kfh:
        for item in range(16):
            byte_val = hexlify(bytes(key_val[item:item+1])).decode().upper()
            #print (byte_val)
            kfh.write (byte_val)
            if (item==15):
                kfh.write("\n")
            else:
                kfh.write(" ")
    #**********************************************************************
    aes_obj.key_load(key_val)
    log_obj.info (f"[+] Success: Key Loading is done successfully  ")

    # Start AES Key exapnsion
    aes_obj.key_gen_start()

    # Check Whether Key expnasion is Done or not ?
    key_exp_status = aes_obj.is_key_exp_done()
    if (key_exp_status == False):
        log_obj.critical (f"[-] Failure. <Key Load Fail> Do Debug, Check, Reset and Run !!!!")
        sys.exit(1)
    else:
        log_obj.info (f"[+] Success: Key Expansion is done successfully")
    
    data_file_name = "data_" + session_key_name + ".txt"
    log_obj.info (f"[+] Data file created: {data_file_name}")

    enc_file_name = "enc_" + session_key_name + ".txt"
    log_obj.info (f"[+] Enc file created: {enc_file_name}")

    if (RANDOM_TEST == True):
        for i in range(TEST_CASES_CNT):  # test cases count
           log_obj.info(f"                                                                             ") 
           log_obj.info(f"#---------------------------------------------------------------------------#")
           log_obj.info(f"#                              TEST CASE-{i+1:4d}                           #") 
           log_obj.info(f"#---------------------------------------------------------------------------#")
           # Load AES Plain Data
           #data_val = DataGenerator(32).get_data()
           #print (f"DBG: {data_val}")
           data= []
           for i in range(16):
               data.append(random.randint(0,255))
           #print (f"Data: {data}")    
           #data_val = b'\x11\x11\x22\x22\x33\x33\x44\x44\x55\x55\x66\x66\x77\x77\x88\x89'
           #********************** DATA FILE ***************************************
           with open (data_file_name,"a+") as dfh:
               for item in range(16):
                   byte_val = hexlify(bytes(data[item:item+1])).decode().upper()
                   #print (byte_val)
                   dfh.write (byte_val)
                   if (item==15):
                       dfh.write("\n")
                   else:
                       dfh.write(" ")
           #**********************************************************************
           aes_obj.data_load(data)
           log_obj.info (f"[+] Success: All Data was written successfully  ")
           
           # Check Whether Data Loading is Done or not ?
           data_load_status = aes_obj.is_data_load_done()
           if (data_load_status == False):
               log_obj.critical (f"[-] Failure. <Data Load Fail> Do Debug, Check, Reset and Run !!!!")
               sys.exit(1)
           else:
               log_obj.info (f"[+] Success: Data Loading is done successfully")
           
           # Start AES Core
           aes_obj.aes_core_start()
           Sakura_AES.total_no_of_cases = Sakura_AES.total_no_of_cases + 1
           log_obj.info (f"[+] Success: AES Core Start is Initiated       ")

           # Wait for AES is done
           aes_done_status = aes_obj.is_aes_done()
           if (aes_done_status == False):
               log_obj.critical (f"[-] Failure. <AES Done Fail> Do Debug, Check, Reset and Run !!!!")
               sys.exit(1)
           else:
               log_obj.info (f"[+] Success: AES is done successfully             ")
           
           # Read Cipher Data
           cipher_data = aes_obj.recv_cipher_data()
           #print (cipher_data)
           #print (type(cipher_data))
           #print (len(cipher_data))
           #********************** CIPHER FILE ***************************************
           with open (enc_file_name,"a+") as efh:
               for item in range(16):
                   byte_val = hexlify(bytes(cipher_data[item:item+1])).decode().upper()
                   #print (byte_val)
                   efh.write (byte_val)
                   if (item==15):
                       efh.write("\n")
                   else:
                       efh.write(" ")
           #**********************************************************************
           aes_obj.data_load(data)
           log_obj.info (f"[+] Success: All Data was written successfully  ")
           log_obj.info (f"[+] Received Cipher Data: X{hexlify(cipher_data).decode().upper()}")

           #compare with Golden Model
           match_status = aes_obj.is_data_match (bytes(key_val),bytes(data),cipher_data,log_obj)
           if match_status == True:
               Sakura_AES.pass_tests = Sakura_AES.pass_tests +1
               log_obj.info (f"[+]Success: Data is matching with Golden Model")
               time.sleep(SLEEP_TIME)  # sleeps 
           else:    
               Sakura_AES.fail_tests = Sakura_AES.fail_tests +1
               log_obj.critical (f"[-]Failure: Data is not matching with Golden Model")
               log_obj.critical (f"------------- CODE EXECUTION IS FAILED ----------")
               sys.exit(1)

    aes_obj.results_summary(log_obj)
    # Close FTDI Device
    ftdi_dev_obj.close_dev()
    log_obj.info (f"[+]FTDI is Shutting down....")
    log_obj.info (f"+==================================================+")
    log_obj.info (f"|        SUCCESSFULLY RAN ALL TEST CASES           |")
    log_obj.info (f"+==================================================+")
