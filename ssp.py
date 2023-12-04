import crcmod
import serial
import time
import sys


ser = serial.Serial("/dev/ttyUSB0", 9600, 8, serial.PARITY_NONE, 2, 1)


SEQ  = 0x80

class ssp():


    def __init__(self):
        self.SEQ = 0x80
        self.arr = []


    def make_packet(self, cmd, length, data):

        new_arr = bytearray()
        new_arr.append(0x7F)
        new_arr.append(self.SEQ)
        new_arr.append(length)
        new_arr.append(cmd)
        if data != None:
            for b in data:
                new_arr.append(b)


        crc16 = crcmod.Crc(0x18005,0xFFFF,False)
        c = new_arr[1:len(new_arr)]
        crc16.update(c)
        vl = crc16.crcValue

        new_arr.append(vl & 0xFF)
        new_arr.append((vl >> 8) & 0xFF)

        tmp = bytearray()
        ind = 0
        for b in new_arr:
            tmp.append(b)
            if b == 0x7F and (ind > 0):
                tmp.append(b)
            ind = ind + 1

        new_arr.clear()
        for b in tmp:
            new_arr.append(b)
   
        ser.write(new_arr)
        #print("Sent:", end = " ")
        for a in new_arr:
            hex(a)[2:]#print(hex(a)[2:], end = ", ")
        #print("\n")


        if self.SEQ == 0x00:
            self.SEQ = 0x80
        elif self.SEQ == 0x80:
            self.SEQ = 0x00
        #else:
            #print("problem with byte 2")

    def response(self):

        ind = 0
        length = 0 
        #print("Response:", end = " ")
        while True:
            value = ser.read()
            #print(value.hex(), end = ", ")
            self.arr.append(ord(value))
            ind = ind + 1
            if ind == 3:
                length = ord(value) + 5
            if ind == length:
                break
        #print("\n")
  
