import serial
import time

port = "COM10"

s = serial.Serial(port, 9600)

s.flushInput()
for i in range(100):
    s.write(b'0')
    time.sleep(0.2)
    s.write(b'1')

s.close()