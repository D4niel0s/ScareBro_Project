import serial

port = "COM10"

s = serial.Serial(port, 9600)

s.flushInput()


inp = int(input("choose song:\t")) #In the real script, this variable will be the output of the classification

s.write(inp.to_bytes())
    
s.close()