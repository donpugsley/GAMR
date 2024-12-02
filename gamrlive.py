# Pugsley tweaks 11/25
import sys
import serial
import io
import time
import numpy as np
import plotille
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

NREAD = 200*17 # must be less than 4095

ser.reset_input_buffer() # Discard any input data

while (1):
    time.sleep(0.1)
    try:
        nw = ser.in_waiting
        if ser.in_waiting > NREAD: # half a second of data
            b = ser.read(NREAD)
            ser.reset_input_buffer() # Discard remaining input data
            D = gamr.decode(b)
            n = len(D[0])
            skips = D[5] # byte offsets of data skips
            #            print(f'Decoded {len(D[0])} points with {len(skips)} data skips')
            # Convert to nT
            x = np.array(D[0])
            x = (x.astype(float)*2*5)/(2**24) # voltage
            x = (x/(5e-3*182.8181818181))*1e5 # nT
            y = np.array(D[1])
            y = (y.astype(float)*2*5)/(2**24)
            y = (y/(5e-3*182.8181818181))*1e5
            z = np.array(D[2])
            z = (z.astype(float)*2*5)/(2**24)
            z = (z/(5e-3*182.8181818181))*1e5
            
            # # Create time, assuming no skips
            # t = np.array(list(range(1,x.size+1)))/SR # Seconds
            # t = t.astype(float)
            
            # f = plotille.Figure()
            # f.width = 60
            # f.height = 30
            # f.set_x_limits(min_=min(t),max_=max(t))
            # mmax = max(max(x),max(y),max(z))
            # mmin = min(min(x),min(y),min(z))
            # f.set_y_limits(min_=mmin,max_=mmax)
            # f.color_mode = 'byte'
            # f.scatter(t,x,lc=25,label='X')
            # f.scatter(t,y,lc=100,label='Y')
            # f.scatter(t,z,lc=200,label='Z')
            # print(f.show(legend=True))
            
            print(f'({len(x)}) X {np.mean(x):.6}\t({len(y)}) Y {np.mean(y):.6} \t({len(z)}) Z {np.mean(z):.6}')
        else:
            print (nw,' ',end="")

        sys.stdout.flush()

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

