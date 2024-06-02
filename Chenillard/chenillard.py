from machine import Pin
import utime

pinNumber1 = 18
pinNumber2 = 22
pinNumber3 = 28

led1 = Pin(pinNumber1, mode = Pin.OUT)
led2 = Pin(pinNumber2, mode = Pin.OUT)
led3 = Pin(pinNumber3, mode = Pin.OUT)

try:
    while True:
        led1.toggle()
        utime.sleep(0.3)
        led1.toggle()
        led2.toggle()
        utime.sleep(0.3)
        led2.toggle()
        led3.toggle()
        utime.sleep(0.3)
        led3.toggle()
except KeyboardInterrupt:
    led1.off()
    led2.off()
    led3.off()
    