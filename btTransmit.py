import serial

port = "COM10"

s = serial.Serial(port, 9600)

s.flushInput()


inp = input("choose song")

if(inp=="1"):
    s.write(b'1')
elif(inp=="2"):
    s.write(b'2')
    
s.close()
