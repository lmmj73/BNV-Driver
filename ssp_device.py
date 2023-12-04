from ssp import ssp
import time

FIRMWARE = 0X20
DATASET = 0X21
SETUP_REQUEST = 0x05
SYNC = 0x11
ENABLE = 0x0A
SET_INHIBITS = 0x02
POLL = 0x07

data = {
    0xF1: "Slave Reset",
    0xEF: "Read",
    0xEE: "Note Credit",
    0xED: "Rejecting",
    0xEC: "Rejected",
    0xCC: "Stacking",
    0xEB: "Stacked",
    0xE9: "Unsafe Jam",
    0xE8: "Disabled",
    0xE6: "Fraud Attempt",
    0xE7: "Stacker Full",
    0xE1: "Note Cleared From Front",
    0xE2: "Note Cleared Into Cashbox",
    0xB5: "Channel Disable",
    0xB6: "Initialising",
    0xA5: "Ticket Printing",
    0xA6: "Ticket Printed",
    0xA8: "Ticket Printing Error",
    0xAE: "Print Halted",
    0xAD: "Ticket In Bezel",
    0xAF: "Printed To Cashbox",
    0xA7: "Ticket In Bezel At Startup",
    0x9E: "Refill Note Credit"
}

_ssp = ssp()
class ssp_device():

    def __init__(self, currency, note_values, poll_response, note_info, loop):
        self.currency = ""
        self.note_values = []
        self.poll_response = ""
        self.note_info = ""
        self.loop = True

    def firmware(self):
        print("Firmware: ", end = "")
        _ssp.make_packet(FIRMWARE,1,None)
        _ssp.response()
        a = hex(_ssp.arr[2])
        for i in range(4,int(a, 16)):
            print(chr(_ssp.arr[i]), end = "")
        _ssp.arr.clear()


    def dataset(self):
        _ssp.arr.clear()
        print("Dataset: ", end = "")
        _ssp.make_packet(DATASET,1,None)
        _ssp.response()
        for i in range(4,_ssp.arr[2]+3):
            print(chr(_ssp.arr[i]), end = "")
        _ssp.arr.clear()
    
    def channels(self):
        _ssp.arr.clear()
        _ssp.make_packet(SETUP_REQUEST,1,None)
        _ssp.response()
        self.currency = str(chr(_ssp.arr[9])) + str(chr(_ssp.arr[10])) + str(chr(_ssp.arr[11]),)
        print(self.currency,end = "")

        n = _ssp.arr[15]#no of channels (3)
        mul = 0

        for i in range(0,3):
            mul = mul + _ssp.arr[12 + i] << (8 * (2 -i))
            
        channel_values = _ssp.arr[16:16+n]
        self.note_values = [i * mul for i in channel_values]
        print(self.note_values)


    def sync(self):
        print("Sync")
        _ssp.make_packet(SYNC,1,None)
        _ssp.response()
        _ssp.arr.clear()


    def enable(self):
        print("Enable")
        _ssp.make_packet(ENABLE,1,None)
        _ssp.response()


    def set_inhibits(self):
        print("Set inhibits")
        _ssp.make_packet(SET_INHIBITS,3, bytearray([0xFF,0xFF]))
        _ssp.response()


    def poll(self):
        self.loop = True
        last_response = ""
        _ssp.arr.clear()
        self.poll_response = ""
        while self.loop:
            _ssp.make_packet(POLL, 1, None)
            _ssp.response()
            if _ssp.arr[2] > 1:
                index = _ssp.arr[2] - 1    
                ind = 0        
                while index > 0:
                    self.poll_response = data.get(_ssp.arr[ind + 4],"Invalid data")         
                    if self.poll_response ==  "Invalid data":
                        x  = 0         
                    if self.poll_response == "Read":
                        self.poll_response = (self.poll_response) + " " + str(_ssp.arr[ind +5])
                        index = index - 1
                        ind = ind + 1                        
                    if  self.poll_response == "Note Credit":    
                        self.poll_response = (self.poll_response) + ": " + str(self.currency + " " + str(self.note_values[int(_ssp.arr[ind +5])-1]))
                        self.note_info = self.poll_response
                        self.loop = False
                        index = index - 1
                        ind = ind + 1
                    if self.poll_response != last_response:
                        print(self.poll_response)       
                        last_response = self.poll_response
                    index = index - 1
                    ind = ind + 1

            time.sleep(0.1)
            _ssp.arr.clear()

