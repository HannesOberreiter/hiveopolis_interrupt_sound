## Python script to generate random sound frequencies ##

### Libraries ###

`numpy, pyaudio, math, time, random, os`

pyaudio --- reference and installation guide:
http://people.csail.mit.edu/hubert/pyaudio/

### sinus.py & sinus-modified.py ###
Plays random order of defined frequencies with given ampltiude (0.5)

`python sinus.py`
`python sinus-modified.py`


### amp.py & amp-modified.py ###
Plays random order of ampltiudes and frequencies

`python amp.py`
`python amp-modified.py`

### environment.py ###
Plays wav files in random order for max. 10s from folder environment.

`python environment.py`

### pulse_from_file.py ###
Plays wav files in random order from folder sound_files.

`python pulse_from_file.py`

### pulse.py ###
Not working code, tested to generate pulsing with our generator class. We use now pulse_form_file.py, which works more precise.

`python pulse.py`

### parameter.xlsx ###
Just a helper file for us to write down possible parameters around the hive, while testing the different virbrations.

### references and citation ###
* portAudio
http://www.portaudio.com/license.html
* pyaudio - python wrapper for portAudio
http://people.csail.mit.edu/hubert/pyaudio/
* Class ToneGenerator
https://markhedleyjones.com/projects/python-tone-generator
