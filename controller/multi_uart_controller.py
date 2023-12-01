import serial
import time
import random

class MultiUARTController():
    """
    This is the Python code to control the MultiUART Controller
    """

    def __init__(self, port):
        self.port = port
        self.secret_code = ['c','h']
        self.active_communication_channel = 0
        self.powered_channels = [0,0,0,0] # Maybe change to only 54
        self.ser = serial.Serial(self.port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1.3, xonxoff=0, rtscts=0)
        if(self.ser.is_open==False):
            self.ser.open()
    
    def transmit_noise(self, count):
        delay = 0.001
        for i in range(count):
            if(self.ser.is_open):
                self.ser.write(chr(random.randint(0,256)).encode())
                time.sleep(delay)       

    def transmit_packet(self, channel_packet, state_packet):
        if(self.ser.is_open):
            self.ser.write(self.secret_code[0].encode()) #character 'c'
            self.ser.write(self.secret_code[1].encode()) #character 'h'
            self.ser.write(chr(channel_packet).encode())
            self.ser.write(chr(state_packet).encode())

    def set_communication_channel(self, channel, baud):
        if(channel <= 7):   #Change to 3
            self.transmit_packet(channel,baud)
            self.active_communication_channel = channel

    def read_byte_on_channel(self, channel):
        if(self.powered_channels[channel]):
            pass
        else:
            self.set_power_to_channel(channel, 1)
        self.read_byte()

    def read_byte(self):
        if(self.powered_channels[self.active_communication_channel]):
            pass
        else:
            self.set_power_to_channel(self.active_communication_channel, 1)
        try:
            return int.from_bytes(self.ser.read(),byteorder='big')
        except Exception as exc:
            print(exc)

    def set_power_to_channel(self, channel, state):
        if(channel <= 7):
            self.transmit_packet(channel+8,state)
            self.powered_channels[channel] = state

    def set_power_to_all_channels(self, state):
        for i in range(0,len(self.powered_channels)):
            self.set_power_to_channel(i, state)
    
    def toggle_power_to_channel(self, channel):
        self.set_power_to_channel(channel, not self.powered_channels[channel])
    
    def toggle_power_to_all_channels(self, reversed = False):
        if reversed:
            for i in range(len(self.powered_channels)-1,0,-1):
                self.toggle_power_to_channel(i)
        else:
            for i in range(0,len(self.powered_channels)):
                self.toggle_power_to_channel(i)

    def knight_rider(self,cycles,delay_time):
        for i in range(0,cycles):
            self.toggle_power_to_all_channels()
            time.sleep(delay_time)
            self.toggle_power_to_all_channels()
            time.sleep(delay_time)
            self.toggle_power_to_all_channels(reversed=True)
            time.sleep(delay_time)
            self.toggle_power_to_all_channels(reversed=True)
            time.sleep(delay_time)