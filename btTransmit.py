import serial

port = "COM10"
s = serial.Serial(port, 9600)

s.reset_input_buffer()

inp = input("choose song:\t").encode() #In the real script, this variable will be the output of the classification
s.write(inp) #inp is of type bytes (encoded string)

s.close()