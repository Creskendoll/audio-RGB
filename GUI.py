from tkinter import *
from audio.AudioWorker import AudioWorker
from audio.WorkerConfig import WorkerConfig

config = WorkerConfig()


def set_gain(gain):
    config.GAIN = float(gain)


def set_min_brightness(b):
    config.MIN_BRIGHTNESS = float(b)


if __name__ == '__main__':
    root = Tk()

    audio_worker = AudioWorker(config)

    ########## GUI ###################################################
    label = Label(root, text="Gain")
    gain_scale = Scale(root, from_=0., to=1., orient=HORIZONTAL,
                       length=200, resolution=0.01, command=set_gain)
    gain_scale.set(config.GAIN)
    label.pack()
    gain_scale.pack()

    label = Label(root, text="Min Brightness")
    min_br_scale = Scale(root, from_=0., to=1., orient=HORIZONTAL,
                         length=200, resolution=0.01, command=set_min_brightness)
    min_br_scale.set(config.MIN_BRIGHTNESS)
    label.pack()
    min_br_scale.pack()

    ########## VISUALIZATION LOOP ##################################################

    audio_worker.start()
    mainloop()
    audio_worker.stop()
