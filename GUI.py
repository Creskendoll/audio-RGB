from tkinter import *
from audio.AudioWorker import AudioWorker
from audio.WorkerConfig import WorkerConfig
import copy
import paramiko
from os import environ

root = Tk()
root.title("LED Config Editor")
config = WorkerConfig()
init_config = copy.deepcopy(config)


def reset_config():
    set_gain(init_config.GAIN)
    set_min_brightness(init_config.MIN_BRIGHTNESS)
    set_threshold(init_config.THRESHOLD)
    set_modulation_attack(init_config.ATTACK)
    set_modulation_decay(init_config.DECAY)
    set_channel_range(init_config.CHANNEL_RANGE_START,
                      init_config.CHANNEL_RANGE_END)


channel_var = IntVar(root, value=config.CHANNEL_RANGE)
gain_var = DoubleVar(root, value=config.GAIN)
min_br_var = DoubleVar(root, value=config.MIN_BRIGHTNESS)
threshold_var = DoubleVar(root, value=config.THRESHOLD)
modulation_attack_var = DoubleVar(root, value=config.ATTACK)
modulation_decay_var = DoubleVar(root, value=config.DECAY)
channel_range_start = IntVar(root, value=config.CHANNEL_RANGE_START)
channel_range_end = IntVar(root, value=config.CHANNEL_RANGE_END)
auto_modulate_var = BooleanVar(root, value=config.AUTO_MODULATE)
display_bars_var = BooleanVar(root, value=config.DISPLAY_BARS)


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


def set_modulation_attack(a):
    config.ATTACK = float(a)
    modulation_attack_var.set(a)


def set_modulation_decay(d):
    config.DECAY = float(d)
    modulation_decay_var.set(d)


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


def start_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.CLIENT, port=22, username="pi",
                password=environ.get("PI_PASS"))
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "nohup python3 Documents/MusicRGB/client.py &")


if __name__ == '__main__':
    SCALE_LEN = 400

    audio_worker = AudioWorker(config)

    ########## GUI ###################################################
    label = Label(root, text="Channel Range")
    channel_range = Scale(root, from_=1, to=1024, orient=HORIZONTAL,
                          length=SCALE_LEN, command=set_channel_no, var=channel_var)
    label.pack()
    channel_range.pack()

    label = Label(root, text="Gain")
    gain_scale = Scale(root, from_=0., to=1., orient=HORIZONTAL,
                       length=SCALE_LEN, resolution=0.01, command=set_gain, var=gain_var)
    label.pack()
    gain_scale.pack()

    label = Label(root, text="Min Brightness")
    min_br_scale = Scale(root, from_=0., to=1., orient=HORIZONTAL,
                         length=SCALE_LEN, resolution=0.01, command=set_min_brightness, var=min_br_var)
    label.pack()
    min_br_scale.pack()

    label = Label(root, text="Threshold")
    threshold_scale = Scale(root, from_=0.01, to=1., orient=HORIZONTAL,
                            length=SCALE_LEN, resolution=0.01, command=set_threshold, var=threshold_var)
    label.pack()
    threshold_scale.pack()

    label = Label(root, text="Modulation Attack")
    modulation_attack_scale = Scale(root, from_=0., to=0.3, orient=HORIZONTAL,
                                    length=SCALE_LEN, resolution=0.0005, command=set_modulation_attack, var=modulation_attack_var)
    label.pack()
    modulation_attack_scale.pack()

    label = Label(root, text="Modulation Decay")
    modulation_decay_scale = Scale(root, from_=0., to=0.3, orient=HORIZONTAL,
                                   length=SCALE_LEN, resolution=0.0005, command=set_modulation_decay, var=modulation_decay_var)
    label.pack()
    modulation_decay_scale.pack()

    label = Label(root, text="Active Channel Start")
    channel_start_scale = Scale(root, from_=0, to=config.CHANNEL_RANGE, orient=HORIZONTAL,
                                length=SCALE_LEN, command=lambda x: set_channel_range(x, channel_range_end.get()), var=channel_range_start)
    label.pack()
    channel_start_scale.pack()

    label = Label(root, text="Active Channel End")
    channel_end_scale = Scale(root, from_=0, to=config.CHANNEL_RANGE, orient=HORIZONTAL,
                              length=SCALE_LEN, command=lambda x: set_channel_range(channel_range_start.get(), x), var=channel_range_end)
    label.pack()
    channel_end_scale.pack()

    display_bars_check = Checkbutton(
        root, text='Display Bars', var=display_bars_var, onvalue=True, offvalue=False, command=set_bars)
    display_bars_check.pack()

    auto_modulate_check = Checkbutton(
        root, text='Auto Modulate', var=auto_modulate_var, onvalue=True, offvalue=False, command=set_auto_modulate)
    auto_modulate_check.pack()

    reset_button = Button(root, text="Reset Config", command=reset_config)
    reset_button.pack()

    client_connect_button = Button(
        root, text="Connect Client", command=start_client)
    client_connect_button.pack()

    ########## VISUALIZATION LOOP ##################################################

    audio_worker.start()
    mainloop()
    audio_worker.stop()
