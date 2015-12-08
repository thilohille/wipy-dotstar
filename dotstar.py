##
## Python module to control for APA102C ledstripes (Adafruit Dotstars) on the Wipy 
## 
##

from machine import SPI
import time

class DotStars:


    def __init__(self, leds):
        self.ledcount = leds
        self.buffersize = self.ledcount * 4
        self.buffer = bytearray(self.ledcount * 4)
        self.emptybuffer = bytearray(self.ledcount * 4)
        for i in range(0, self.buffersize, 4):
            self.emptybuffer[i] = 0xff
            self.emptybuffer[i + 1] = 0x0
            self.emptybuffer[i + 2] = 0x0
            self.emptybuffer[i + 3] = 0x0   
        self.startframe = bytes([0x00, 0x00, 0x00, 0x00])
        self.endframe   = bytes([0xff, 0xff, 0xff, 0xff])
        self.spi = SPI(0, mode=SPI.MASTER, baudrate=8000000, polarity=0, phase=0,bits=8, firstbit=SPI.MSB)
        self.clearleds()

       
    #init empty self.buffer
    def clearleds(self):
        self.buffer = self.emptybuffer[:]

    def setled(self, led, red=0, green=0, blue=0, bri=0x1f):
        if (led > self.ledcount):
            led=led % self.ledcount
        
        if (led < 0):
            led = self.ledcount + led
        
        frameheader = (0x07 << 5) | bri
        offset = led * 4
        self.buffer[offset] = frameheader
        self.buffer[offset + 1] = blue
        self.buffer[offset + 2] = green
        self.buffer[offset + 3] = red

    def send(self):
        #self.spi.write(self.startframe + self.buffer + self.endframe)
        self.spi.write(self.startframe + self.buffer)
 


if __name__ == '__main__':
    ###Demo        
    import os
    Dotty = DotStars(60) 
    Dotty.send()
    bri = 1
    while True:
        #create some random colors
        r1=ord(os.urandom(1))
        r2=ord(os.urandom(1))
        r3=ord(os.urandom(1))
        for i in range(0,Dotty.ledcount):
            Dotty.clearleds()
            Dotty.setled(led=i, red=r1, green=r2, blue=r3)
            Dotty.setled(led=Dotty.ledcount - 1 - i, red=r3, green=r2, blue= r1)
            Dotty.setled(led=(Dotty.ledcount // 2) - (i // 2), red=r2, green=r1, blue= r3)
            Dotty.setled(led=(Dotty.ledcount // 2) + (i // 2), red=r2, green=r1, blue= r3)
            Dotty.send()
            time.sleep_ms(20)
         
