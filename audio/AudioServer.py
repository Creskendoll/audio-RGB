########## LIBRARIES ###########################################################

# import Console
import scipy.fftpack
from scipy import average
import pyaudio
import time
import struct
import json
import socket
import time
from scipy import pi, signal

# import serial
import struct
import time
from misc.helpers import *

########## SETTINGS ##############################################

# Loudness detect:
# frequency channel of the FFT to use (see console output to decide)
CHANNEL_RANGE = 15
CHANNEL_RANGE_START = 0
CHANNEL_RANGE_END = 3
GAIN = 0.2       # audio gain (multiplier)
THRESHOLD = 0.2  # audio trigger threshold

ATTACK = 0.008  # amount of rowdz increase with loudness
DECAY = 0.006   # amount of rowdz decay

# Brightness:
MODULATION = 0.1        # amount of loudness flickering modulation
MIN_BRIGHTNESS = 0.3    # minimum brightness

# Hue mapping:
MIN_HUE = 0
MAX_HUE = 360
# Note that the hue mapping is actually a power function,
# so it will spend more time towards the MIN_HUE, and only a short time towards the MAX_HUE.

########## APPLICATION SETTINGS ################################################

# COM_PORT = 'COM3'   # COM port to use, or None to run without an arudino
COM_PORT = None

# Audio capture settings
SAMPLE_RATE = 96000
BUFFER_SIZE = 2**12     # Changing this will change the frequency response of the algorithm
CUTOFF_FREQ = 20000     # LPF freq (Hz)

CLIENT = '192.168.1.69'  # UDP Client

########## GUI ###################################################

########## CODE ################################################################

# Create LPF filter
# norm_pass = 2*math.pi*CUTOFF_FREQ/SAMPLE_RATE
# norm_stop = 1.5*norm_pass
# (N, Wn) = signal.buttord(wp=norm_pass, ws=norm_stop, gpass=2, gstop=30, analog=0)
# (b, a) = signal.butter(N, Wn, btype='low', analog=0, output='ba')
# b *= 1e3

# Open Audio stream (uses default audio adapter)
# Windows
p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
#                 input_device_index=2, input=True, output=False, frames_per_buffer=BUFFER_SIZE)

# Linux
# On linux use pavucontrol and audacity to configure the speakers as a recording device
# 1) In audacity set recorder to alsa and start monitoring
# 2) Run pavucontrol and tick the Monitor Input device you want to capture
stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                input=True, frames_per_buffer=BUFFER_SIZE)

# UDP broadcast
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 44444))

########## GLOBAL VARIABLES ####################################################

red = 0
green = 0
blue = 0

noisiness = 0       # Noisiness level

falling = False     # Is modulation rising or falling

########## VISUALIZATION LOOP ##################################################

while True:
    ## Part 1: Sample Audio ##

    # cur_time = time.time()
    # Get audio sample
    buf = stream.read(BUFFER_SIZE)
    data = scipy.array(struct.unpack("%dh" % (BUFFER_SIZE), buf))

    ## Part 2: Perform FFT and Filtering ##

    # Filter incoming data
    # data = signal.lfilter(b,a,data)

    # Generate FFT
    freqs, y = get_fft(data, BUFFER_SIZE, SAMPLE_RATE)

    # Average the samples
    # y=smoothMemory(y,3)

    # Normalize
    y = y / 5

    # Average into chunks of N
    yy = [scipy.average(y[n:int(n+CHANNEL_RANGE)])
          for n in range(0, len(y), CHANNEL_RANGE)]
    # Discard half of the samples, as they are mirrored
    yy = yy[:len(yy)//2]

    # Loudness detection
    channels_avg = sum(yy[CHANNEL_RANGE_START:CHANNEL_RANGE_END])
    loudness = thresh(channels_avg * GAIN, THRESHOLD)

    # Noisiness meter
    if falling:
        noisiness -= loudness * DECAY
    else:
        noisiness += loudness * ATTACK

    noisiness = limit(noisiness, 0.0, 1.0)

    # Brightness modulation
    modulation = MODULATION * limit(noisiness, 0.0, 1.0)
    brightness = limit(MIN_BRIGHTNESS + (1. -
                                         MIN_BRIGHTNESS) * loudness, 0.0, 1.0)

    # Hue modulation (power relationship)
    # mapping = (10 ** limit(noisiness, 0.0, 1.0)) / 10.0
    # mapping = mapping * 1.1 - 0.11

    # Linear mapping
    mapping = (10 * limit(noisiness, 0.0, 1.0)) / 10.0

    hue = mapval(mapping, 0.0, 1.0, MIN_HUE, MAX_HUE)

    if noisiness > 0.99:
        falling = True
    elif noisiness < 0.01:
        falling = False

    # Display colour
    red, green, blue = hsv2rgb(hue, 1.0, brightness)

    # if COM_PORT:
    #     RGB.update([int(red),int(green),int(blue)])

    # Debug information
    labels = list(yy)
    bars = list(yy)
    labels.extend(['-', 'loud', 'noise', 'map', 'brght',
                   '-', 'hue', 'red', 'grn', 'blue'])
    bars.extend([0, loudness, noisiness, mapping, brightness, 0,
                 hue/360.0, red/255.0, green/255.0, blue/255.0])

    update_bars(labels, bars)

    colors = {
        "time": 0,
        "red": red,
        "green": green,
        "blue": blue
    }
    msg = json.dumps(colors).encode('utf-8')
    server.sendto(msg, (CLIENT, 37020))
