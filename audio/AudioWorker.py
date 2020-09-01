from threading import Thread
from StateEnum import StateEnum
from scipy import average, array, pi, signal
import struct
from audio.WorkerConfig import WorkerConfig
import pyaudio
from misc.SignalTransmiter import SignalTransmiter
from misc.helpers import *


class AudioWorker(object):

    # Takes in a Queue pointer
    def __init__(self, config: WorkerConfig):
        # Keep thread None when not being used
        self.running = False
        self.config = config
        self.falling = False     # Is modulation rising or falling
        self.noisiness = 0

        self.transmitter = SignalTransmiter()

        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=config.SAMPLE_RATE,
                             input=True, frames_per_buffer=config.BUFFER_SIZE)

    def updateConfig(self, config: WorkerConfig):
        self.config = config

    # Start listening
    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self._run, args=())
            self.thread.start()

    # Stop listening
    def stop(self):
        if self.running:
            # Stop and reset the thread
            self.running = False
            self.thread.join()

    # Runs async and populates the queue with states and strings
    def _run(self):
        MAX_CHANNEL_NO = 1024
        # Run continuously
        while self.running:
            config = self.config
            ## Part 1: Sample Audio ##

            # cur_time = time.time()
            # Get audio sample
            buf = self.stream.read(config.BUFFER_SIZE)
            data = array(struct.unpack("%dh" % (config.BUFFER_SIZE), buf))

            ## Part 2: Perform FFT and Filtering ##

            # Filter incoming data
            # data = signal.lfilter(b,a,data)

            # Generate FFT
            freqs, y = get_fft(data, config.BUFFER_SIZE, config.SAMPLE_RATE)

            # Average the samples
            # y = smoothMemory(y, 5)

            # Normalize
            y = y / 5

            DIVIDE_BY = MAX_CHANNEL_NO // config.CHANNEL_RANGE
            # Average into chunks of N
            yy = [average(y[n:int(n+DIVIDE_BY)])
                  for n in range(0, len(y), DIVIDE_BY)]
            # Discard half of the samples, as they are mirrored
            yy = yy[:len(yy)//2]

            # Loudness detection
            channels_sum = sum(
                yy[config.CHANNEL_RANGE_START:config.CHANNEL_RANGE_END]) / (config.CHANNEL_RANGE_END - config.CHANNEL_RANGE_START)
            loudness = thresh(channels_sum * config.GAIN, config.THRESHOLD)

            # Noisiness meter
            if self.falling:
                if config.AUTO_MODULATE:
                    self.noisiness -= config.DECAY
                else:
                    self.noisiness -= loudness * config.DECAY
            else:
                if config.AUTO_MODULATE:
                    self.noisiness += config.ATTACK
                else:
                    self.noisiness += loudness * config.ATTACK

            self.noisiness = limit(self.noisiness, 0.0, 1.0)

            # Brightness modulation
            br_value = config.MIN_BRIGHTNESS + \
                (1. - config.MIN_BRIGHTNESS) * loudness
            brightness = limit(br_value, 0.0, 1.0)

            # Hue modulation (power relationship)
            # mapping = (10 ** limit(noisiness, 0.0, 1.0)) / 10.0
            # mapping = mapping * 1.1 - 0.11

            # Linear mapping
            mapping = limit(self.noisiness, 0.0, 1.0)

            hue = mapval(mapping, 0.0, 1.0, config.MIN_HUE, config.MAX_HUE)

            if self.noisiness > 0.99:
                self.falling = True
            elif self.noisiness < 0.01:
                self.falling = False

            # Display colour
            red, green, blue = hsv2rgb(hue, 1.0, brightness)

            if config.DISPLAY_BARS:
                # Debug information
                labels = list(yy)
                bars = list(yy)
                labels.extend(['-', 'loud', 'noise', 'map', 'brght',
                               '-', 'hue', 'red', 'grn', 'blue'])
                bars.extend([0, loudness, self.noisiness, mapping, brightness, 0,
                             hue/360.0, red/255.0, green/255.0, blue/255.0])

                update_bars(labels, bars)

            config.current_led_color = (red, green, blue)
            config.is_boi_active = brightness > config.BOI_THRESHOLD

            colors = {
                "boi": str(config.is_boi_active),
                "red": red,
                "green": green,
                "blue": blue
            }

            self.transmitter.send(colors, config.CLIENT)
