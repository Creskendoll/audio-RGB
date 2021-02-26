class WorkerConfig(object):
    def __init__(self):
        super().__init__()
        self.current_led_color = (0, 0, 0)
        self.is_boi_active = False
        # Loudness detect:
        # frequency channel of the FFT to use (see console output to decide)
        self.MAX_CHANNEL_NO = 1024

        self.CHANNEL_RANGE = 150
        self.CHANNEL_RANGE_START = 0
        self.CHANNEL_RANGE_END = 3
        self.GAIN = 0.6       # audio gain (multiplier)
        self.THRESHOLD = 0.2  # audio trigger threshold

        self.BOI_THRESHOLD = 0.9  # audio trigger threshold

        self.ATTACK = 0.002  # amount of rowdz increase with loudness
        self.DECAY = 0.002   # amount of rowdz decay
        self.JUMP_THRESHOLD = 0.9
        self.HUE_OFFSET = 0.1
        self.PEAK_TIME_MARGIN = 150

        # Brightness:
        self.MIN_BRIGHTNESS = 0.2    # minimum brightness

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

        self.DISPLAY_BARS = True
        self.AUTO_MODULATE = True
