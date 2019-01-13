import serial
import time
ArduinoSerial=serial.Serial("COM8", 4800)
def func():
	arduiOp=str(ArduinoSerial.readline())
	#print(arduiOp)
	l=[arduiOp[2],arduiOp[3]]
	return l
	