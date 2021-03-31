import time
import picokeypad as keypad
import machine

keypad.init()
keypad.set_brightness(0.1)

led = machine.Pin(25, machine.Pin.OUT)

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

NUM_PADS = keypad.get_num_pads()

for i in range(0, NUM_PADS):
    r = BUTTONS[i][COL][R]
    g = BUTTONS[i][COL][G]
    b = BUTTONS[i][COL][B]
    keypad.illuminate(i, r, g, b)
keypad.update()


def send_keypress(param):
    pass


while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            for button in range(0, NUM_PADS):
                # check if this button is pressed and no other buttons are pressed
                if button_states & 0x01 > 0:
                    if not (button_states & (~0x01)) > 0:
                        send_keypress(BUTTONS[button][KEY])
                    break
                button_states >>= 1
    led.toggle()
    time.sleep(0.1)
