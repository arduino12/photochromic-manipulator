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
2. Learn the basics from the [**presentation**](https://docs.google.com/presentation/d/1GHex3-h8UOdAG93ix5lFpUwPYDLUTp-qcYMy1NBWBzI/) and visit some of it's links.
3. View [**S2-Mini schematics**](https://www.wemos.cc/en/latest/_static/files/sch_s2_mini_v1.0.0.pdf) and [**pm_v2**](https://drive.google.com/file/d/1oIQLA3CALWdbSq6uK5VD0ayfpmH0RfYR/view) schematics.
### Software and Firmware
## [**!! See a video of all the following steps !!**](https://drive.google.com/file/d/1aEj5KBWeWXW5ZsfGAlvBMZWhSd8E85TE/view?usp=drive_link)
1. Install a MicroPython IDE, lets go with [**Thonny IDE**](https://thonny.org/). (here are [other options](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/) FYI).
2. Download MicroPython [**LOLIN_S2_MINI.bin**](https://micropython.org/resources/firmware/LOLIN_S2_MINI-20230426-v1.20.0.bin) firmware file for our [ESP32-S2 microcontroller](https://www.wemos.cc/en/latest/s2/s2_mini.html). (taken from [here](https://micropython.org/download/LOLIN_S2_MINI/)).  
(Use [**LOLIN_S2_MINI_ESPNOW.bin**](https://github.com/glenn20/micropython-espnow-images/raw/main/20230427-v1.20.0-espnow-2-gcc4c716f6/firmware-esp32-LOLIN_S2_MINI.bin) firmware file instead if you want suppont for the `espnow` example).
3. **Press the small boot button (marked "0" on PCB)** while connecting the microcontroller to computer via USB-C cable.
4. [Flash the firmware file to the microcontroller using Thonny](https://linuxhint.com/micropython-esp32-thonny-ide/#2), wait for "Done" message.  
  **4.1** Press the tribar [≡] button and select `Select local MicroPython image...` and select `LOLIN_S2_MINI_ESPNOW.bin`.  
  **4.2** Press the tribar [≡] button and select `Show install options` to set `Target address` to `0x1000...`).  
  **4.3** Press the `Install` button!**
6. **Press the small reset button (marked "RST" on PCB)**.
7. Press the red "Stop" button in Thonny - now the microcontroller MicroPython REPL prompt should appear in Thonny terminal!
8. Download this [repository](https://github.com/arduino12/photochromic-manipulator/archive/refs/heads/main.zip) and extract it (delete the compressed zip file).
9. Upload the content of micropython folder to the microcontroller using Thonny.  
   **9.1** Press View (top menu-bar) and select `Files`, do the same with `Object inspector`.
   **9.2** Navigate to the path of the unzipped `photochromic-manipulator/micropython`.
   **9.3** Select all files -> right-click -> `Upload to /` and make sure all were copied to the device. 
11. Run an example by writing `from examples.basic import test_leds` and press Enter,  
can also run by opening the file and pressing F5.

