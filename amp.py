#############################
# Hiveopolis - frequency generator
# for dance interrupt experiment
#############################

# Amplitude change testing

import numpy
### pyaudio --- see link for installation guide
### http://people.csail.mit.edu/hubert/pyaudio/
import pyaudio
import math
import time
import random
import os

# define our clear function
# https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# Tone Generator (https://markhedleyjones.com/projects/python-tone-generator)
class ToneGenerator(object):

    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out

    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False

    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)

# init our class object
generator = ToneGenerator()
# define start and endpoint of frequencies, with step in range
#frequency_start = 50
#frequency_end = 800
#steps = 50
# Time (seconds) to play at each step
step_duration = 5

# create list array of frequencies
frequency_array = list([50, 500, 5000])

# Kammerton A
# frequency_array.extend([440])
# D5
# frequency_array.extend([587.33])

# Amplitude of the waveform


amplitude_array = list([0, 0.25, 0.5, 0.75, 1])

total_array = []
for n in range(0, len(frequency_array)):
    for x in range(0, len(amplitude_array)):
        total_array.append([frequency_array[n], amplitude_array[x]])

# array_list [n][0] === Frequency
# array_list [n][1] === Amplitude


# Number of runs
runs = 4
# clear
clear()

print('######  Hiveopolis ######')
print('Starting in 4 minutes ...')
#time.sleep(240)
time.sleep(5)
clear()

for i in range(1, runs + 1):

    # print starting sequence
    print('Hiveopolis run: ' + str(i))
    print('Starting in 5 seconds ...')
    time.sleep(5)
    clear()
    # shuffle our total array of frequencies and amplitudes
    random.shuffle(total_array)

    for x in range(0, len(total_array)):
        # print current loop number
        print("Run: " + str(i) + " - Loop: " + str(x+1) + " / " +  str(len(total_array)))

        print("Vibration on: {0:0.2f} Hz".format(total_array[x][0]) + " and {0:0.2f} amplitude".format(total_array[x][1]))

        generator.play(total_array[x][0], step_duration, total_array[x][1])
        while generator.is_playing():
            # record the sound?
            pass

        print("Vibration off: 10 seconds")
        time.sleep(10)
        clear()


print('######  Hiveopolis ######')
print('######   Finished  ######')
time.sleep(240)
clear()
