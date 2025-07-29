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

encoder_handler.pins = ((board.D3, board.D4, board.D5),)

keyboard.volume = 32  # Startovací hlasitost 0–100
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

    # Představme si, že máme proměnnou pro sledování mute
    if keyboard.is_muted:
        oled.write("Mute")
    else:
        oled.write(f"Volume: {keyboard.volume}")

# OLED nastavení
oled_ext = Oled(
    i2c=board.I2C(),  # využije D6 (SDA), D7 (SCL) pokud máš základní setup
    width=128,
    height=32,
    to_display=draw_volume,
    flip=False,
    display_mode=OledDisplayMode.MASTER
)

keyboard.extensions.append(oled_ext)


# --- Define rows and columns (example pins, adjust if needed!) ---
keyboard.col_pins = (board.A3, board.A2, board.A1)
keyboard.row_pins = (board.D1, board.D2)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Add MediaKeys (optional) ---
keyboard.extensions.append(MediaKeys())

# --- RGB setup ---
rgb = RGB(pixel_pin=board.D0, num_pixels=16, hue_default=100)
keyboard.extensions.append(rgb)

# --- Keymap: 2x3 ---
keyboard.keymap = [
    [
        KC.CTRL_C,              # Kopírovat
        KC.WIN_D,               # Zobrazit plochu
        KC.CTRL_V,              # Vložit
        KC.MEDIA_PLAY_PAUSE,    # Přehrát/Pauza
        KC.CTRL_Z,              # Zpět
        KC.CTRL_S               # Uložit
    ]
]


if __name__ == '__main__':
    keyboard.go()
