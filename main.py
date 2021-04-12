# Adapted from Sandy J Macdonald's gist at https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90 to configure all buttons and switch off all lights in loop

import time
import board
import busio
import usb_hid

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from digitalio import DigitalInOut, Direction, Pull

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)


lit = 0
last_button_states = 0
colour_index = 0
RED = (0x80, 0x00, 0x00)
RED0 = (0x20, 0x00, 0x00)
RED1 = (0x30, 0x00, 0x00)
RED2 = (0x40, 0x00, 0x00)
RED3 = (0x50, 0x00, 0x00)
RED4 = (0x60, 0x00, 0x00)
RED5 = (0x70, 0x00, 0x00)
RED6 = (0x80, 0x00, 0x00)
RED7 = (0x90, 0x00, 0x00)
RED8 = (0xA0, 0x00, 0x00)
RED9 = (0xB0, 0x00, 0x00)
BLUE = (0x00, 0x00, 0x80)
WHITE = (0x80, 0x80, 0x80)
BLACK = (0x00, 0x00, 0x00)
YELLOW = (0x80, 0x80, 0x00)
CYAN = (0x00, 0x80, 0x80)
MAGENTA = (0x80, 0x00, 0x80)
R=0
G=1
B=2
BUTTONS = [(RED0, Keycode.KEYPAD_ZERO),
           (RED1, Keycode.KEYPAD_ONE),
           (RED2, Keycode.KEYPAD_TWO),
           (RED3, Keycode.KEYPAD_THREE),

           (RED4, Keycode.KEYPAD_FOUR),
           (RED5, Keycode.KEYPAD_FIVE),
           (RED6, Keycode.KEYPAD_SIX),
           (RED7, Keycode.KEYPAD_SEVEN),

           (RED8, Keycode.KEYPAD_EIGHT),
           (RED9, Keycode.KEYPAD_NINE),
           (WHITE, Keycode.UP_ARROW),
           (CYAN, Keycode.GRAVE_ACCENT),

           (MAGENTA, Keycode.M),
           (BLACK, None),
           (WHITE, Keycode.DOWN_ARROW),
           (YELLOW, Keycode.SPACEBAR),
          ]
COL=0
KEY=1

def button_colour(i):
    r = BUTTONS[i][COL][R]
    g = BUTTONS[i][COL][G]
    b = BUTTONS[i][COL][B]
    return (r, g, b)

def bright(rgb):
    return ((int)(rgb[0]*1.5), (int)(rgb[1]*1.5), (int)(rgb[2]*1.5))

def dim(rgb):
    return ((int)(rgb[0]*0.5), (int)(rgb[1]*0.5), (int)(rgb[2]*0.5))

for i in range(0, num_pixels):
    pixels[i] = dim(button_colour(i))

# Works up to here

# TODO: Keyboard stuff

def read_button_states(x, y):
    pressed = [0] * 16
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed

held = [0] * 16
while True:
    pressed = read_button_states(0, 16)
    button_pressed = False
    for i in range(0, num_pixels):
        if pressed[i]:
            print("Button pressed", i)
            button_pressed = True
            pixels[i] = bright(button_colour(i))

            if not held[i]:
                kbd.send(BUTTONS[i][KEY])
                held[i] = 1

    if not button_pressed:
        for i in range(16):
            pixels[i] = dim(button_colour(i))
            held[i] = 0  # Set held states to off

    time.sleep(0.1)  # Debounce
