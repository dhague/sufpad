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
RED0 = (0x10, 0x00, 0x00)
RED1 = (0x20, 0x00, 0x00)
RED2 = (0x30, 0x00, 0x00)
RED3 = (0x40, 0x00, 0x00)
RED4 = (0x50, 0x00, 0x00)
RED5 = (0x60, 0x00, 0x00)
RED6 = (0x70, 0x00, 0x00)
RED7 = (0x80, 0x00, 0x00)
RED8 = (0x90, 0x00, 0x00)
RED9 = (0xA0, 0x00, 0x00)
BLUE = (0x00, 0x00, 0x80)
WHITE = (0x80, 0x80, 0x80)
BLACK = (0x00, 0x00, 0x00)
YELLOW = (0x80, 0x80, 0x00)
CYAN = (0x00, 0x80, 0x80)
MAGENTA = (0x80, 0x00, 0x80)
R=0
G=1
B=2
BUTTONS = [(RED0, "0"), (RED1, "1"), (RED2, "2"), (RED3, "3"),
           (RED4, "4"), (RED5, "5"), (RED6, "6"), (RED7, "7"),
           (RED8, "8"), (RED9, "9"), (WHITE, "UP"), (CYAN, "`"),
           (MAGENTA, "m"), (BLACK, None), (WHITE, "DOWN"), (YELLOW, " "),
          ]
COL=0
KEY=1

for i in range(0, num_pixels):
    r = BUTTONS[i][COL][R]
    g = BUTTONS[i][COL][G]
    b = BUTTONS[i][COL][B]
    pixels[i] = (r, g, b)

# Works up to here

# TODO: Keyboard stuff

def colourwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


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

    if pressed[0]:
        pixels[0] = colourwheel(0 * 16)  # Map pixel index to 0-255 range

        if not held[0]:
            layout.write("volu")
            kbd.send(Keycode.ENTER)
            # held[0] = 1

    elif pressed[1]:
        pixels[1] = colourwheel(1 * 16)  # Map pixel index to 0-255 range

        if not held[1]:
            layout.write("mpc next")
            kbd.send(Keycode.ENTER)
            held[1] = 1

    elif pressed[2]:
        pixels[2] = colourwheel(2 * 16)  # Map pixel index to 0-255 range

        if not held[2]:
            layout.write("rad4")
            kbd.send(Keycode.ENTER)
            held[2] = 1

    elif pressed[3]:
        pixels[3] = colourwheel(3 * 16)  # Map pixel index to 0-255 range

        if not held[3]:
            layout.write("mpc next")
            kbd.send(Keycode.ENTER)
            held[3] = 1

    elif pressed[4]:
        pixels[4] = colourwheel(4 * 16)  # Map pixel index to 0-255 range

        if not held[4]:
            layout.write("vold")
            kbd.send(Keycode.ENTER)
            # held[4] = 1

    elif pressed[5]:
        pixels[5] = colourwheel(5 * 16)  # Map pixel index to 0-255 range

        if not held[5]:
            layout.write("mpc prev")
            kbd.send(Keycode.ENTER)
            held[5] = 1

    elif pressed[6]:
        pixels[6] = colourwheel(6 * 16)  # Map pixel index to 0-255 range

        if not held[6]:
            layout.write("rad3")
            kbd.send(Keycode.ENTER)
            held[6] = 1

    elif pressed[7]:
        pixels[7] = colourwheel(7 * 16)  # Map pixel index to 0-255 range

        if not held[7]:
            layout.write("mpc prev")
            kbd.send(Keycode.ENTER)
            held[7] = 1

    elif pressed[8]:
        pixels[8] = colourwheel(8 * 16)  # Map pixel index to 0-255 range

        if not held[8]:
            layout.write("toggle_disp1")
            kbd.send(Keycode.ENTER)
            held[8] = 1

    elif pressed[9]:
        pixels[9] = colourwheel(9 * 16)  # Map pixel index to 0-255 range

        if not held[9]:
            layout.write("mpc stop")
            kbd.send(Keycode.ENTER)
            held[9] = 1

    elif pressed[10]:
        pixels[10] = colourwheel(10 * 16)  # Map pixel index to 0-255 range

        if not held[10]:
            layout.write("rad2")
            kbd.send(Keycode.ENTER)
            held[10] = 1

    elif pressed[11]:
        pixels[11] = colourwheel(11 * 16)  # Map pixel index to 0-255 range

        if not held[11]:
            layout.write("mpc stop")
            kbd.send(Keycode.ENTER)
            held[11] = 1

    elif pressed[12]:
        pixels[12] = colourwheel(12 * 16)  # Map pixel index to 0-255 range

        if not held[12]:
            layout.write("ssh pi\"192.168.9.97 picade_switch")
            kbd.send(Keycode.ENTER)
            held[12] = 1

    elif pressed[13]:
        pixels[13] = colourwheel(13 * 16)  # Map pixel index to 0-255 range

        if not held[13]:
            layout.write("mpc toggle")
            kbd.send(Keycode.ENTER)
            held[13] = 1

    elif pressed[14]:
        pixels[14] = colourwheel(14 * 16)  # Map pixel index to 0-255 range

        if not held[14]:
            layout.write("rad1")
            kbd.send(Keycode.ENTER)
            held[14] = 1

    elif pressed[15]:
        pixels[15] = colourwheel(15 * 16)  # Map pixel index to 0-255 range

        if not held[15]:
            layout.write("mpc toggle")
            kbd.send(Keycode.ENTER)
            held[15] = 1

    else:  # Released state
        for i in range(16):
            pixels[i] = (0, 0, 0)  # Turn pixels off
            held[i] = 0  # Set held states to off
        time.sleep(0.1)  # Debounce
