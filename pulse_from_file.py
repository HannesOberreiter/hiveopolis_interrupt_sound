#############################
# Hiveopolis - take audio files and play them in a certain order
# for dance interrupt experiment - pulsing
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

runs = 4
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


#file_array = ["16bit5000hz30sek1amp.wav","16bit5000hz30sek1amp_pulse09seksil01sec.wav", "16bit5000hz30sek00625amp_pulse09seksil01sec.wav", "16bit5000hz30sec00625amp.wav" ]
file_array = ["16bit500hz1min1amp.wav","16bit500hz1min1amp_pulse09seksil01sec.wav", "16bit5000hz1min1amp_pulse09seksil01sec.wav", "16bit5000hz1min1amp.wav" ]

print('######  Hiveopolis ######')
print('Starting in 4 minutes ...')
time.sleep(240)
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
        f = wave.open(r"sound_files/{}".format(j),"rb")

        # if j == "16bit5000hz30sek1amp.wav":
        #     a = "(FRQ = 5,000hz, AMP = 1)"
        # if j == "16bit5000hz30sek1amp_pulse09seksil01sec.wav":
        #     a = "(FRQ = 5,000hz, AMP = 1, PULSE = 0.9:0.1sec)"
        # if j == "16bit5000hz30sec00625amp.wav":
        #     a = "(FRQ = 5,000hz, AMP = 0.0625)"
        # if j == "16bit5000hz30sek00625amp_pulse09seksil01sec.wav":
        #     a = "(FRQ = 5,000hz, AMP = 0.0625, PULSE = 0.9:0.1sec)"

        if j == "16bit500hz1min1amp.wav":
            a = "(FRQ = 500hz, AMP = 1, 60s)"
        if j == "16bit500hz1min1amp_pulse09seksil01sec.wav":
            a = "(FRQ = 500hz, AMP = 1, PULSE = 0.9:0.1sec, 60s)"
        if j == "16bit5000hz1min1amp_pulse09seksil01sec.wav":
            a = "(FRQ = 5,000hz, AMP = 1, PULSE = 0.9:0.1sec, 60s)"
        if j == "16bit5000hz1min1amp.wav":
            a = "(FRQ = 5,000hz, AMP = 1, 60s)"

        loop = loop + 1
        print("Run: " + str(i) + " - Loop: " + str(loop) + " / " +  str(len(file_array)))
        print("Playing {}".format(a))

        #open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        #read data
        data = f.readframes(chunk)

        #play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        #stop stream
        stream.stop_stream()
        stream.close()


        print("Vibration off: 30 seconds")
        time.sleep(30)
        clear()

p.terminate()
print('######  Hiveopolis ######')
print('######   Finished  ######')
time.sleep(240)
clear()
