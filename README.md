# audio-RGB

A program to control LEDs using voice commands with a Raspberry PI. The purpose of this project is to control a RGB led strip via a microphone.
This project is optimized and built for the Raspberry PI but can be modified to fit various applications.

## Installation

The project is written with Python 3.6. Pyaudio doesn't support Python 3.7 at the time of developing this project.

Run this command to install PyAudio on Debian/Ubuntu systems:

-   `sudo apt-get install python3-pyaudio`

You need `pip` in order to install dependencies.

The required packages are listed in the `req.txt` file.
Run this command in order to install necessary packages:

-   `pip install -r requirements.txt`

The project depends on [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) which might need to be installed using the package manager on Debian/Ubuntu systems.

## Running

Clone the repo on your Raspberry PI and run `client.py`. Note down the IP address/hostname of your PI since you'll need it to connect to the PI from the server.
On the server, run `main.py`, put in the address of your PI and click "Set Client".

Play around with the settings to find the optimal balance.

## Wiring of LEDs

You have to plug in the RGB connectors of your LEDs to the respective pins of your Raspberry PI.

-   Red -> GPIO 16
-   Green -> GPIO 20
-   Blue -> GPIO 21

If you're running a LED which requires more than 5V to work, then you need an external power supply.

[Refer to this page for the Raspberry PI pinout.](https://pinout.xyz/)

## Speech recognition module

Run `speech.py` to start the program. You have to have a microphone attach to your device. If you have more than one recording devices, you can set the `device_index` found in `Audio.py` file.

The program will automatically detect speech and use Google's services to convert audio to text.

Try running this if you get an error:

-   `sudo apt-get install portaudio19-dev`

Project depends the SpeechRecognition library which uses Google's services to turn sound into text.
