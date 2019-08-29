#############################
# Hiveopolis - frequency generator
# for dance interrupt experiment
#############################

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
frequency_start = 100
frequency_end = 800
steps = 50
# Time (seconds) to play at each step
step_duration = 5
# create list array of frequencies
frequency_array = list(range(frequency_start, frequency_end, steps))

# add special cases to array
frequency_array.extend([1000])
frequency_array.extend([1500])
frequency_array.extend([2000])
frequency_array.extend([2500])
# white noise
frequency_array.extend([0])
def white_noise():
    stream = pyaudio.PyAudio().open(format = pyaudio.paInt8,channels = 1,rate = 22050,output = True)
    for n in range(0,220000,1): stream.write(chr(int(random.random()*256)))
# Kammerton A
frequency_array.extend([440])
# D5
frequency_array.extend([587.33])

# Amplitude of the waveform
amplitude = 0.50
# Number of runs
runs = 4
# clear
clear()

for i in range(1, runs + 1):

    # print starting sequence
    print('Hiveopolis run: ' + str(i))
    print('Starting in 5 seconds ...')
    time.sleep(5)
    clear()
    # shuffle our frequencies in array
    random.shuffle(frequency_array)

    for x in range(0, len(frequency_array)):
        # print current loop number
        print("Loop - " + str(x+1) + " / " +  str(len(frequency_array)))
        # special case white noise
        if(frequency_array[x] == 0):
            print("Playing white noise")
            white_noise()
        else:
            # custom prints for special cases
            if(frequency_array[x] == 440):
                print("Playing concert pitch A")
            elif(frequency_array[x] == 587.33):
                print("Playing concert pitch A")
            else:
                # standard print of current frequency
                print("Playing tone at {0:0.2f} Hz".format(frequency_array[x]))

            # use our generator class to generate the sound
            generator.play(frequency_array[x], step_duration, amplitude)
            while generator.is_playing():
                # record the sound?
                pass

        print("Sleep 10 seconds")
        time.sleep(10)
        clear()
