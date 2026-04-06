import colorsys
import random


def generate_color(hue: int | None = None, saturation: int = 75, lightness: int = 75) -> str:
    h = (hue if hue is not None else random.randint(0, 359)) / 360
    s = saturation / 100
    l = lightness / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))
