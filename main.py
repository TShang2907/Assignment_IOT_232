from modbus485 import*
from mqtt import*
import time
import serial as serial

try:
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
except:
    print("Modbus485**","Failed to write data")

m485 = Modbus485(ser)
relay1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

m485.modbus485_send(relay1_ON)
time.sleep(2)
m485.modbus485_send(relay1_OFF)
time.sleep(2)
m485.modbus485_send(relay2_ON)
time.sleep(2)
m485.modbus485_send(relay2_OFF)
time.sleep(2)
m485.modbus485_send(relay3_ON)
time.sleep(2)
m485.modbus485_send(relay3_OFF)
time.sleep(2)

while True:
    m485.modbus485_read_adc()

