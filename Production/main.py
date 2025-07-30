import board
import digitalio
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.peg_oled_display import Oled,OledDisplayMode,OledReactionType, OledReaction
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.modules.encoder import EncoderHandler


keyboard = KMKKeyboard()

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = ((board.D3, board.D4), board.D2)

keyboard.volume = 35 # Start volume
keyboard.is_muted = False

def vol_up():
    if keyboard.volume < 100:
        keyboard.volume += 5
    keyboard.is_muted = False
    return KC.VOLU

def vol_down():
    if keyboard.volume > 0:
        keyboard.volume -= 5
    keyboard.is_muted = False
    return KC.VOLD

def toggle_mute():
    keyboard.is_muted = not keyboard.is_muted
    return KC.MUTE

encoder_handler.map = [((vol_up, vol_down), toggle_mute)]


def draw_volume(oled):
    from kmk.handlers.sequences import simple_key_sequence
    from kmk.keys import KC

    if keyboard.is_muted:
        oled.write("Mute")
    else:
        oled.write(f"Volume: {keyboard.volume}")

# OLED settings
oled_ext = Oled(
    i2c=board.I2C(),  # Uses D6, D7
    width=128,
    height=32,
    to_display=draw_volume,
    flip=False,
    display_mode=OledDisplayMode.MASTER
)

keyboard.extensions.append(oled_ext)


# Define keys matrix
keyboard.col_pins = (board.A0, board.A1, board.A2)
keyboard.row_pins = (board.D29, board.D0)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.extensions.append(MediaKeys())

# LEDs
rgb = RGB(pixel_pin=board.D1, num_pixels=16, hue_default=64)
keyboard.extensions.append(rgb)

keyboard.keymap = [
    [
        KC.CTRL_C,              # copy
        KC.WIN_D,               # homescreen
        KC.CTRL_V,              # paste
        KC.MEDIA_PLAY_PAUSE,    # Play/Pause
        KC.CTRL_Z,              # Undo
        KC.CTRL_S               # Save
    ]
]


if __name__ == '__main__':
    keyboard.go()