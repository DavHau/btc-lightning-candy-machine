### Bitcoin Lightning Candy Machine, The Easy Way
This project is inspired by https://github.com/arcbtc/1.21 and uses the same hardware.
The code is written from scratch in MicroPython and can be deployed on any MicroPython compatible board like NodeMCU (esp32) or similar ones.
https://www.opennode.co/ is used as custodial backend for creating payment requests for the Bitcoin Lightning Network.

#### Installation:
1. Flash MicroPython onto the esp32 board (Instructions: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
2. Get a REPL promt. (Instructions: https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html)
3. Connect the board to your wifi network and enable webREPL. This is required to upload files to the device.
4. Use the upload.py script to upload the project files to the board
