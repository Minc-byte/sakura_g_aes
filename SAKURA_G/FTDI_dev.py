#---------------------------------------------------------
# Module Name   : FTDI_dev
# Designer      : Inc
# Ver           : v2
# History       :
#
#-------------------------------------------------------
import ftd2xx
import sys

class FTDI_dev():
    def __init__(self,dev_id =b'FT6AQ0JZA', rd_time_out=5000, wr_time_out=50000):
        if (dev_id == None):
            print (f"[-] Error: Wrong Device ID!")
            sys.exit()
        else:
            self.config_device(dev_id, rd_time_out,wr_time_out)
            if (self.dev_obj == None):
                print (f"[-] Error: Device Might be disconnected!")
                sys.exit()

    def config_device (self,dev_id,rd_time_out,wr_time_out):
        try:
            self.dev_obj      = ftd2xx.openEx(dev_id)
            self.rd_time_out  = rd_time_out
            self.wr_time_out  = wr_time_out
            self.dev_obj.setTimeouts (self.rd_time_out,self.wr_time_out)
            self.dev_obj.purge (ftd2xx.defines.PURGE_TX | ftd2xx.defines.PURGE_RX)
        except ftd2xx.ftd2xx.DeviceError:
            print (f"[-] Dev Error: Device Might be Disconnected/ Powered OFF.\nTerminating ....")
            sys.exit()
        else:    
            print (f"[+] FTDI Dev Configuration is done")

    def send_data (self,tx_data):
        #print (f"[ + ] Writing <{len(tx_data)}> bytes to FPGA")
        bytes_written = self.dev_obj.write (tx_data)
        #print (f"[ + ] {bytes_written} bytes writeen successfully")

    def recv_data(self,cnt):
        rx_data = self.dev_obj.read(cnt)
        #print (f"[ + ] Received <{len(rx_data)}> bytes from FPGA")
        return rx_data

    def close_dev (self):
        #print (f"[ + ] FTDI Device is shutting down ....")
        self.dev_obj.close()

    def  device_summary(self): # may be imlemented in later phases
        pass

if __name__ == "__main__":
    obj = FTDI_dev(b'FT6AQ0JZA')
    obj.send_data (b'abcd')
    print (obj.recv_data(2))
    print (obj.recv_data(2))
    obj.close_dev()
