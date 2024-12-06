import serial
import io
import numpy as np
import gamrlib as gamr

SR = 2000

ser = serial.Serial(
    port = "/dev/ttyS4",
    baudrate = 500000,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.01
)

# Set up buffered reader
BUFSEC = 5 # Delay at startup is to fill this entirely
READSEC = 0.2
buffered_reader = io.BufferedReader(ser,buffer_size=int(BUFSEC*2000*17)) # Hold 

while (1):
    try:
        b = buffered_reader.read(int(READSEC*2000*17)) # First call reads a buffer full
        D = gamr.decode(b)
        x = D[0]
        y = D[1]
        z = D[2]
        temp = D[3]
        pps = D[4]
        sign = D[5]

        print('X ',f'{np.mean(x):.6}', '\tY ',f'{np.mean(y):.6}', '\tZ ',f'{np.mean(z):.6}')
        
    except KeyboardInterrupt:
        ser.close()
        buffered_reader.close()
    except:
        ser.close()
        buffered_reader.close()


## parse input arguments 
#parser = argparse.ArgumentParser()
#parser.add_argument("filename",nargs='?',default='gamr.bin')
#args = parser.parse_args()
#output_file = args.filename
#
## create buffer object
#buffer = io.BytesIO()
#
## lock for thread safe access to buffer
#buffer_lock = threading.Lock()
#
## flag to signal threads to stop
#stop_threads = threading.Event()
#
#def read_from_serial():
#    global buffer
#    while not stop_threads.is_set():
#        if ser.in_waiting > 0:
#            with buffer_lock:
#                buffer.write(ser.read(ser.in_waiting))
#
#        
#def save_data_to_file():
#    global buffer
#    with open(output_file,'wb') as f:
#        while not stop_threads.is_set():
#            with buffer_lock:
#                buffer.seek(0)
#                data = buffer.read() # read all available bytes
#                f.write(data)
#                buffer.seek(0) # go back to beginning of buffer
#                buffer.truncate(0) # clear buffer
##                time.sleep(0.01)
#
#def decode_data():
#    global buffer
##    with open(output_file,'wb') as f:
#    while not stop_threads.is_set():
#        with buffer_lock:
#            buffer.seek(0)
#            data = buffer.read() # read all available bytes
#                  
#            buffer.seek(0) # go back to beginning of buffer
#            buffer.truncate(0) # clear buffer
#
#try:
#    # create and start threads
#    read_thread = threading.Thread(target = read_from_serial)
##    save_thread = threading.Thread(target = decode_data)
#    read_thread.start()
# #   save_thread.start()
#    
#    # Allow threads to run indefinitely
#    read_thread.join()
#  #  save_thread.join()
#
#except KeyboardInterrupt:
#    print("exiting")
#    stop_threads.set()
#    read_thread.join()
#   # save_thread.join()
#finally:
#    ser.close()
#    print("port closed")

