# Pugsley tweaks 11/25
import sys
# Open the GAMR serial port and write a command
import serial
import io
import sys

if len(sys.argv) < 2:
    print ('Available commands:')
    print ('  S - Start/Stop DAQ')
    print ('  D - Restore default settings (Sinc5,2000,analog,none)')
    print ('  O,F/S5,n - Configure filter (F FIR, S5 Sinc5) and data rate (1 500, 2 2000)')
    print ('  X,n - Configure ADC input MUX source (1 analog, 2 +FS, 3 short, 4 -FS)')
    print ('  M,n - Configure modulation mode (1 none, 2 bidirectional')
    exit()
    
cmd = sys.argv[1]

cmd = bytes('!' + cmd + '\r\n','utf-8')

#debugging... print(cmd,end="")

ser = serial.Serial(
    port = "/dev/ttyS4",
    baudrate = 500000,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.01
)

ser.reset_output_buffer() # Discard any pre-existing write data
ser.write(cmd)



