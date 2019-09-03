#############################
# Hiveopolis - take audio files and play them in a certain order
# for dance interrupt experiment - enviroment
#############################

import numpy
### pyaudio --- see link for installation guide
### http://people.csail.mit.edu/hubert/pyaudio/
import pyaudio
import math
import time
import random
import os
import wave
import glob

runs = 11
# define our clear function
# https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# clear
clear()

#define stream chunk
chunk = 1024

file_array = sorted(glob.iglob('environment/*.wav'))

print('######  Hiveopolis ######')
print('Starting in 4 minutes ...')
#time.sleep(240)
clear()
#instantiate PyAudio
p = pyaudio.PyAudio()

for i in range(1, runs + 1):

    # print starting sequence
    print('Hiveopolis run: ' + str(i))
    print('Starting in 5 seconds ...')
    time.sleep(5)
    clear()

    # shuffle our frequencies in array
    random.shuffle(file_array)
    loop = 0
    for j in file_array:
        loop = loop + 1
        f = wave.open(j,"rb")

        a = j.replace('environment/', '')

        print("Run: " + str(i) + " - Loop: " + str(loop) + " / " +  str(len(file_array)))
        print("Playing {} for 10 seconds".format(a))

        # open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        # read data
        data = f.readframes(chunk)
        stream.write(data)

        #play stream
        start = time.time()
        while data:
            if((time.time()- start) > 10):
                break
            stream.write(data)
            data = f.readframes(chunk)

        #stop stream
        stream.stop_stream()
        stream.close()

        print("Vibration off: 10 seconds")
        time.sleep(10)
        clear()

p.terminate()
print('######  Hiveopolis ######')
print('######   Finished  ######')
time.sleep(240)
clear()
