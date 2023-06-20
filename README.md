# Photochromic Manipulator
A self assembly kit that draw on a photochromic paper!  
Designed and programed with ❤ by [Arad.E](https://github.com/arduino12/) and [Jerusalem Science Museum](https://mada.org.il/) team.

## Technologies
* **Photochemistry:**  
The photochromic pigment in the paper darken its color for a while after being exposed to ultraviolet (UV) light.
* **Kinematics:**  
The LED moves on the paper using a mechanism called [Five-Bar-Planar-Parallel Manipulator](https://en.wikipedia.org/wiki/Five-bar_linkage).
* **Electro-mechanics:**  
The [servo motors](https://gabbyshimoni.wixsite.com/arduino-programming/blank-18) convert electric current into rotary motion.
* **Electro-optics:**  
The UV-LED converts an electric current into UV light.

## Getting started
### Hardware
1. Assemble the kit by following the assembly guide.
### Software and Firmware
* See a video of all the following steps.
1. Install a MicroPython IDE, lets go with [**Thonny IDE**](https://thonny.org/). (here are [other options](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/) FYI).
2. Download MicroPython [**LOLIN_S2_MINI.bin**](https://micropython.org/resources/firmware/LOLIN_S2_MINI-20230426-v1.20.0.bin) firmware file for our [ESP32-S2 microcontroller](https://www.wemos.cc/en/latest/s2/s2_mini.html). (taken from [here](https://micropython.org/download/LOLIN_S2_MINI/)).
3. **Press the small boot button (marked "0" on PCB)** while connecting the microcontroller to computer via USB-C cable.
4. [Flash the firmware file to the microcontroller using Thonny](https://linuxhint.com/micropython-esp32-thonny-ide/#2), wait for "Done" message.
5. **Press the small reset button (marked "RST" on PCB)**.
6. Press the red "Stop" button in Thonny - now the microcontroller MicroPython REPL prompt should appear in Thonny terminal!
7. Download this [repository](https://github.com/arduino12/photochromic-manipulator/archive/refs/heads/main.zip) and extract it (delete the compressed zip file).
8. Upload the content of micropython folder to the microcontroller using Thonny.
9. Run an example by writing `from examples import test_leds`, can also run by opening the file and pressing F5.

