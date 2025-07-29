import board
import digitalio
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.peg_oled_display import Oled,OledDisplayMode,OledReactionType, OledReaction
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# --- Define rows and columns (example pins, adjust if needed!) ---
keyboard.col_pins = (board.A3, board.A2, board.A1)
keyboard.row_pins = (board.D1, board.D2)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Add Layers module (optional) ---
layers = Layers()
keyboard.modules.append(layers)

# --- Add MediaKeys (optional) ---
keyboard.extensions.append(MediaKeys())

# --- RGB setup ---
rgb = RGB(pixel_pin=board.D0, num_pixels=16, hue_default=100)
keyboard.extensions.append(rgb)

# --- Keymap: 2x3 ---
keyboard.keymap = [
    [
        KC.ESC,  KC.ENT, KC.SPC,
        KC.A,    KC.B,   KC.C
    ]
]

if __name__ == '__main__':
    keyboard.go()
