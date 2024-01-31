"""!
@file square.py
This file produces a square wave out of the C0 pin with a period of 10 seconds
"""
import micropython
import utime
import math

# run this file as main file
if __name__ == '__main__':
    # set up C0 pin by creating Pin object
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    
    # run infinite loop
    while True:
       # set the pin to logic high
       pinC0.high()
       # wait for 5 seconds
       utime.sleep_ms(5000)
       # set the pin to logic low
       pinC0.low()
       # wait for 5 seconds
       utime.sleep_ms(5000)


