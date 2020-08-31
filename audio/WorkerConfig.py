class WorkerConfig(object):
    def __init__(self):
        super().__init__()
        # Loudness detect:
        # frequency channel of the FFT to use (see console output to decide)
        self.CHANNEL_RANGE = 15
        self.CHANNEL_RANGE_START = 0
        self.CHANNEL_RANGE_END = 3
        self.GAIN = 0.2       # audio gain (multiplier)
        self.THRESHOLD = 0.2  # audio trigger threshold

        self.ATTACK = 0.008  # amount of rowdz increase with loudness
        self.DECAY = 0.006   # amount of rowdz decay

        # Brightness:
        self.MODULATION = 0.1        # amount of loudness flickering modulation
        self.MIN_BRIGHTNESS = 0.3    # minimum brightness

        # Hue mapping:
        self.MIN_HUE = 0
        self.MAX_HUE = 360
        # Note that the hue mapping is actually a power function,
        # so it will spend more time towards the MIN_HUE, and only a short time towards the MAX_HUE.
        ########## APPLICATION SETTINGS ################################################
        # Audio capture settings
        self.SAMPLE_RATE = 96000
        # Changing this will change the frequency response of the algorithm
        self.BUFFER_SIZE = 2**12
        self.CUTOFF_FREQ = 20000     # LPF freq (Hz)

        self.CLIENT = '192.168.1.69'  # UDP Client
