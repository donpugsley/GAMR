# Serial data acquisition to file for George Valdes GAMR sensor
# Takes a filename, use  `date +'%Y%m%d-%H%M%S'.bin` if you want
# Defaults to GAMR-YYYYMMDDHHMMSS.bin if nothing provided

import serial
import io
import threading
import argparse
import time
import datetime

ser = serial.Serial(
    port = "/dev/ttyS4",
    baudrate = 500000,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.01
)

# create a default filename using date and time

dfn = datetime.datetime.now().strftime("GAMR-%Y%m%d%H%M%SUTC.bin")

# parse input arguments to format file name to datetime
parser = argparse.ArgumentParser()
parser.add_argument("filename",nargs='?',default=dfn)
args = parser.parse_args()
output_file = args.filename

# create buffer object
buffer = io.BytesIO()

# lock for thread safe access to buffer
buffer_lock = threading.Lock()

# flag to signal threads to stop
stop_threads = threading.Event()

def read_from_serial():
    global buffer
    while not stop_threads.is_set():
        if ser.in_waiting > 0:
            with buffer_lock:
                buffer.write(ser.read(ser.in_waiting))

        
def save_data_to_file():
    global buffer
    with open(output_file,'wb') as f:
        while not stop_threads.is_set():
            with buffer_lock:
                buffer.seek(0)
                data = buffer.read() # read all available bytes
                f.write(data)
                buffer.seek(0) # go back to beginning of buffer
                buffer.truncate(0) # clear buffer
#                time.sleep(0.01)

try:
    # create and start threads
    read_thread = threading.Thread(target = read_from_serial)
    save_thread = threading.Thread(target = save_data_to_file)
    read_thread.start()
    save_thread.start()
    
    # Allow threads to run indefinitely
    read_thread.join()
    save_thread.join()

except KeyboardInterrupt:
    print("exiting")
    stop_threads.set()
    read_thread.join()
    save_thread.join()
finally:
    ser.close()
    print("port closed")

