#!/usr/bin/env python
# coding: utf-8

import numpy as np

from colormath.color_objects import HSVColor, sRGBColor
from colormath.color_conversions import convert_color

# [x] basic full value HSV palette
# [x] fibonacci spiral n colours
# [ ] include colorblind range


class PaletteBuilder():

    @classmethod
    def spiral_a(self, r, m):
        # Return angular position as a function of radius
        # r: radius
        # m: revolutions
        return 2*np.pi*r*m

    @classmethod
    def spiral_xy(self, r, m):
        # Return x, y position as a function of radius
        # r: radius
        # m: revolutions
        a = spiral_a(r, m)
        return r*np.cos(a), r*np.sin(a)

    @classmethod
    def lin_H(self, n):
        stop = 360*(1-1/n)
        return np.linspace(0, stop, n)

    @classmethod
    def lin_r(self, n):
        return np.linspace(0, 1, n)

    @classmethod
    def gen_full_palette(self, n_colours):
        # Generate a ring of colours with full saturation and value
        return [HSVColor(i, 1, 1) for i in self.lin_H(n_colours)]

    @classmethod
    def gen_spiral_palette(self, n_colours, turns):
        V = self.lin_r(n_colours)
        H = self.spiral_a(V, turns)*360/(2*np.pi)
        return [HSVColor(h, 1, v) for h, v in zip(H, V)]

    @classmethod
    def to_rgb_values(C):
        return C.rgb_r, C.rgb_g, C.rgb_b

    def __init__(self, n_colours=2, colour_scheme='standard'):

        self.HSV_palette = []

        if colour_scheme == 'standard':
            self.HSV_palette = self.gen_full_palette(n_colours)
        elif colour_scheme == 'spiral':
            colours_per_turn = 10
            n_turns = 1 + n_colours // colours_per_turn
            self.HSV_palette = self.gen_spiral_palette(n_colours, n_turns)

    def get_hsv_values(self):
        return [HSV.get_value_tuple() for HSV in self.HSV_palette]

    def get_rgb_palette(self):
        # Convert palette to RGB
        return [convert_color(HSV, sRGBColor) for HSV in self.HSV_palette]

    def get_rbg_hex_str(self):
        return [RGB.get_rgb_hex().upper() for RGB in self.get_rgb_palette()]


    def optimise_spiral(self):

        def score():




if __name__ == "__main__":
    palette = PaletteBuilder(n_colours=40, colour_scheme='spiral')
    hex_strs = palette.get_rbg_hex_str()
    [print(h) for h in hex_strs]