# audio-RGB

A program to control LEDs using voice commands with a Raspberry PI. The purpose of this project is to control a RGB led strip via a microphone.
This project is optimized and built for the Raspberry PI but can be modified to fit various applications.

## Installation
The project is written with Python 3.6. Pyaudio doesn't support Python 3.7 at the time of developing this project. 

You need `pip` in order to install dependencies.

The required packages are listed in the `req.txt` file. 
Run this command in order to install necessary packages:
- `pip install -r req.txt`
  
The project depends on [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) which might need to be installed using the package manager on Debian/Ubuntu systems.

Run this command to install PyAudio on Debian/Ubuntu systems:
- `sudo apt-get install python-pyaudio python3-pyaudio`

## Running
Run `main.py` to start the program. You have to have a microphone attach to your device. If you have more than one recording devices, you can set the `device_index` found in `Audio.py` file.

The program will automatically detect speech and use Google's services to convert audio to text.

Try running this if you get an error:
- `sudo apt-get install portaudio19-dev`

## Structure
The code is separated into 2 major parts, audio and visual. The audio module deals with the speech to text work while the visual module handles the LEDs. Audio processing is done asynchronously to enable the main thread to change states independently. 

## Wiring of LEDs
You have to plug in the RGB connectors of your LEDs to the respective pins of your Raspberry. The pins can be provided to the Led constructor.

- Red -> 14(TXD)
- Green -> 15(RXD)
- Blue -> 18(PWM0)

If you're running a LED which requires more than 5V to work, then you need an external power supply.

[Refer to this page for the Raspberry PI pinout.](https://pinout.xyz/)

### Speech recognition
Project depends the SpeechRecognition library which uses Google's services to turn sound into text.
