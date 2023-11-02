from tkinter import *
from tkinter.ttk import Style
from audio.AudioWorker import AudioWorker
from audio.WorkerConfig import WorkerConfig
from copy import deepcopy
from paramiko import SSHClient, AutoAddPolicy
from os import path

root = Tk()
root.title("LED Config Editor")
# root.iconphoto(False, PhotoImage(file=path.dirname(
#     path.realpath(__file__)) + '/icon.jpg'))
# root.iconbitmap(path.dirname(
#     path.realpath(__file__)) + '/icon.jpg')
style = Style(root)
style.theme_use('clam')
config = WorkerConfig()
init_config = deepcopy(config)


def reset_config():
    set_gain(init_config.GAIN)
    set_min_brightness(init_config.MIN_BRIGHTNESS)
    set_threshold(init_config.THRESHOLD)
    set_boi_threshold(init_config.BOI_THRESHOLD)
    set_modulation_attack(init_config.ATTACK)
    set_modulation_decay(init_config.DECAY)
    set_channel_range(init_config.CHANNEL_RANGE_START,
                      init_config.CHANNEL_RANGE_END)


channel_var = IntVar(root, value=config.CHANNEL_RANGE)
gain_var = DoubleVar(root, value=config.GAIN)
min_br_var = DoubleVar(root, value=config.MIN_BRIGHTNESS)
threshold_var = DoubleVar(root, value=config.THRESHOLD)
boi_threshold_var = DoubleVar(root, value=config.BOI_THRESHOLD)
modulation_attack_var = DoubleVar(root, value=config.ATTACK)
modulation_decay_var = DoubleVar(root, value=config.DECAY)
peak_time_var = IntVar(root, value=config.PEAK_TIME_MARGIN)
channel_range_start = IntVar(root, value=config.CHANNEL_RANGE_START)
channel_range_end = IntVar(root, value=config.CHANNEL_RANGE_END)
auto_modulate_var = BooleanVar(root, value=config.AUTO_MODULATE)
display_bars_var = BooleanVar(root, value=config.DISPLAY_BARS)
client_var = StringVar(root, value=config.CLIENT)


def set_channel_no(n):
    config.CHANNEL_RANGE = int(n)
    channel_var.set(n)


def set_gain(g):
    config.GAIN = float(g)
    gain_var.set(g)


def set_min_brightness(b):
    config.MIN_BRIGHTNESS = float(b)
    min_br_var.set(b)


def set_threshold(t):
    config.THRESHOLD = float(t)
    threshold_var.set(t)


def set_boi_threshold(t):
    config.BOI_THRESHOLD = float(t)
    boi_threshold_var.set(t)


def set_modulation_attack(a):
    config.ATTACK = float(a)
    modulation_attack_var.set(a)


def set_modulation_decay(d):
    config.DECAY = float(d)
    modulation_decay_var.set(d)


def set_peak_time(d):
    config.PEAK_TIME_MARGIN = int(d)
    peak_time_var.set(d)


def set_bars():
    config.DISPLAY_BARS = display_bars_var.get()


def set_auto_modulate():
    config.AUTO_MODULATE = auto_modulate_var.get()


def set_channel_range(channel_min, channel_max):
    if int(channel_min) < int(channel_max) and int(channel_max) <= config.CHANNEL_RANGE:
        config.CHANNEL_RANGE_START = int(channel_min)
        config.CHANNEL_RANGE_END = int(channel_max)
        channel_range_start.set(channel_min)
        channel_range_end.set(channel_max)


def set_client():
    config.CLIENT = client_var.get()

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


if __name__ == '__main__':
    SCALE_LEN = 400

    audio_worker = AudioWorker(config)

    ########## GUI ###################################################

    #################### Intensity ####################

    intensity_frame = LabelFrame(root, text="Intensity")
    intensity_frame.pack(fill="both", expand="yes")

    label = Label(intensity_frame, text="Gain")
    gain_scale = Scale(intensity_frame, from_=0.001, to=1., orient=HORIZONTAL,
                       length=SCALE_LEN, resolution=0.01, command=set_gain, var=gain_var)
    label.pack()
    gain_scale.pack()

    label = Label(intensity_frame, text="Min Brightness")
    min_br_scale = Scale(intensity_frame, from_=0., to=1., orient=HORIZONTAL,
                         length=SCALE_LEN, resolution=0.01, command=set_min_brightness, var=min_br_var)
    label.pack()
    min_br_scale.pack()

    label = Label(intensity_frame, text="Threshold")
    threshold_scale = Scale(intensity_frame, from_=0.01, to=1., orient=HORIZONTAL,
                            length=SCALE_LEN, resolution=0.01, command=set_threshold, var=threshold_var)
    label.pack()
    threshold_scale.pack()

    label = Label(intensity_frame, text="BOI Threshold")
    boi_threshold_scale = Scale(intensity_frame, from_=0., to=1., orient=HORIZONTAL,
                                length=SCALE_LEN, resolution=0.01, command=set_boi_threshold, var=boi_threshold_var)
    label.pack()
    boi_threshold_scale.pack()

    boi_indicator = Button(
        intensity_frame, width=2, height=2, text="BOI", bg="#000000")
    boi_indicator["state"] = DISABLED
    boi_indicator.pack()

    #################### Channels ####################

    channels_frame = LabelFrame(root, text="Channels")
    channels_frame.pack(fill="both", expand="yes")

    label = Label(channels_frame, text="Channel Range")
    channel_range = Scale(channels_frame, from_=1, to=1024, orient=HORIZONTAL,
                          length=SCALE_LEN, command=set_channel_no, var=channel_var)
    label.pack()
    channel_range.pack()

    label = Label(channels_frame, text="Active Channel Start")
    channel_start_scale = Scale(channels_frame, from_=0, to=config.CHANNEL_RANGE, orient=HORIZONTAL,
                                length=SCALE_LEN, command=lambda x: set_channel_range(x, channel_range_end.get()), var=channel_range_start)
    label.pack()
    channel_start_scale.pack()

    label = Label(channels_frame, text="Active Channel End")
    channel_end_scale = Scale(channels_frame, from_=0, to=config.CHANNEL_RANGE, orient=HORIZONTAL,
                              length=SCALE_LEN, command=lambda x: set_channel_range(channel_range_start.get(), x), var=channel_range_end)
    label.pack()
    channel_end_scale.pack()

    #################### Modulation ####################

    modulation_frame = LabelFrame(root, text="Modulation")
    modulation_frame.pack(fill="both", expand="yes")

    label = Label(modulation_frame, text="Modulation Attack")
    modulation_attack_scale = Scale(modulation_frame, from_=0., to=0.2, orient=HORIZONTAL,
                                    length=SCALE_LEN, resolution=0.0005, command=set_modulation_attack, var=modulation_attack_var)
    label.pack()
    modulation_attack_scale.pack()

    label = Label(modulation_frame, text="Modulation Decay")
    modulation_decay_scale = Scale(modulation_frame, from_=0., to=0.2, orient=HORIZONTAL,
                                   length=SCALE_LEN, resolution=0.0005, command=set_modulation_decay, var=modulation_decay_var)
    label.pack()
    modulation_decay_scale.pack()

    label = Label(modulation_frame,
                  text="Peak Delta Time Margin (Milliseconds)")
    modulation_time_margin = Scale(modulation_frame, from_=1, to=500, orient=HORIZONTAL,
                                   length=SCALE_LEN, command=set_peak_time, var=peak_time_var)
    label.pack()
    modulation_time_margin.pack()

    auto_modulate_check = Checkbutton(
        modulation_frame, text='Auto Modulate', var=auto_modulate_var, onvalue=True, offvalue=False, command=set_auto_modulate)
    auto_modulate_check.pack()

    display_bars_check = Checkbutton(
        root, text='Display Bars', var=display_bars_var, onvalue=True, offvalue=False, command=set_bars)
    display_bars_check.pack()

    client_frame = Frame(root)
    client_text_box = Entry(client_frame, textvariable=client_var).grid(row=0, column=0)
    client_connect_button = Button(
        client_frame, text="Set Client", command=set_client).grid(row=0, column=1)
    client_frame.pack()

    reset_button = Button(root, text="Reset Config", command=reset_config)
    reset_button.pack()

    color = Button(
        root, width=50, height=2, text="", bg=rgb_to_hex(config.current_led_color))
    color["state"] = DISABLED
    color.pack()

    ########## VISUALIZATION LOOP ##################################################

    audio_worker.start()

    running = True

    def exit_app():
        global running
        running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", exit_app)

    while running:
        try:
            color.configure(bg=rgb_to_hex(config.current_led_color))
            boi_color = "#FFFFFF" if config.is_boi_active else "#000000"
            boi_indicator.configure(bg=boi_color)
            root.update_idletasks()
            root.update()
        except:
            exit_app()

    audio_worker.stop()
