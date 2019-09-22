import scipy
from scipy.fftpack import fft,rfft,rfftfreq,fftfreq
import math
import os
clear = lambda: os.system('clear')

def tobyte(i):
    """
    Clip values that fall outside an unsigned byte
    """
    i = int(i)
    if i < 0: i = 0
    if i > 255: i = 255
    return i
    
def limit(val, vmin, vmax):
    """
    Clip values that fall outside vmin & vmax
    """
    if val < vmin: return vmin
    if val > vmax: return vmax
    return val

def mapval(val, minin, maxin, minout, maxout):
    """
    Linear value mapping between in and out
    """
    norm = (val-minin)/(maxin-minin)
    return norm*(maxout-minout) + minout
    
def thresh(val, threshold):
    """
    A bit hard to describe, but this will return 0 
    when val is below the threshold, and will
    linearly map val to anything higher than threshold.
    The effect being that above the threshold, louder
    signals will have more of an effect.
    """
    val -= threshold
    if val < 0: val = 0
    val *= (1.0/threshold)
    return val
    
def hsv2rgb(h, s, v):
    """
    Convert H,S,V to R,G,B
    H: 0.0 to 360.0, S&V: 0.0 to 1.0
    R,G,B: 0 to 255
    """
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)    
    return r, g, b
    
def get_fft(data, bufferSize, sampleRate):
    """
    Run the sample through a FFT, and normalize
    """
    FFT = fft(data)
    freqs = fftfreq(bufferSize*2, 1.0/sampleRate)
    #y = 20*scipy.log10(abs(FFT))/ 100

    y = abs(FFT[0:int(len(FFT)/2)])/1000
    y = scipy.log(y) - 2
    return (freqs,y)
    
ffts=[]
def smoothMemory(ffty,degree=3):
    """
    Average samples. Taken from Python FFT tutorial
    """
    global ffts
    ffts = ffts+[ffty]
    if len(ffts) <=degree: return ffty
    ffts=ffts[1:]
    return scipy.average(scipy.array(ffts),0)
    

bar_len = 70
def update_bars(x,y):
    """
    Display a bar graph in the console
    """
    clear()
    for i,_ in enumerate(y):
        a = int(min(max(y[i],0),1)*bar_len)

        label = str(x[i])[:5]
        label = ' '*(5-len(label)) + label

        text =  label +'[' + ('#'*a) + (' '*(bar_len-a)) + ']' + str(i)
        print(text)
        # console.text(0, i+3, text)

