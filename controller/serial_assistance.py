import serial.tools.list_ports
from configuration_manager import ConfigurationManager
from multi_uart_controller import MultiUARTController
import serial_assistance as sa
import time

def list_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def list_ports_by_description():
    ports = list_ports()
    for p in ports:
        print(p.description)

def get_port_by_name(name):
    available_ports = list_ports()
    selected_port = None
    for p in available_ports:
        if name in p.description:
            selected_port = str(p.device)
    return selected_port