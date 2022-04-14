#!/bin/env python

import numpy as np
from scipy.optimize import minimize

from colormath.color_objects import LabColor, sRGBColor, HSLColor
from colormath.color_diff import delta_e_cie1994
from colormath.color_conversions import convert_color

def cie_delta(hsv1, hsv2):
    from colormath.color_conversions import convert_color
    lab1 = convert_color(hsv1, LabColor)
    lab2 = convert_color(hsv2, LabColor)
    return delta_e_cie1994(lab1, lab2)

def generate_palette(n, jac_d=1, S=1, L=0.5, full_comparison=False):
    # Returns uniform HSV and LAB optimised colours for a
    # palette of n distinct colours.

    from collections import namedtuple
    from itertools import combinations
    
    def adjacent_pairwise_score(h):
        # Objective function for set of hues
        H = [HSLColor(i, S, L) for i in sorted(h)]
        return np.sqrt(np.sum(np.square([1/cie_delta(H[i % len(H)], H[(i+1)%len(H)]) for i,_ in enumerate(H)])))

    def full_pairwise_score(h):
        # Objective function for set of hues
        H = combinations([HSLColor(i, S, L) for i in h], 2) # Generate every pair combination
        return np.sqrt(np.sum(np.square([1/cie_delta(h1, h2) for h1, h2 in H])))

    # Minimise the pairwise difference score between all colours.
    if full_comparison:
        objective_function = adjacent_pairwise_score
    else:
        objective_function = full_pairwise_score
    
    def jac(h):
        # Jacobian (gradient) with respect to each hue
        j = [None for i in h]
        for i, hi in enumerate(h):
            D = np.zeros(np.size(h))#[0 for j in h]
            D[i] = jac_d
            j[i] = (objective_function(h+D) - objective_function(h))/jac_d
        return j
    
    initial_hues = np.linspace(0, 360*(1-1/n), n)
    
    solution = minimize(objective_function, initial_hues, jac=jac)
    
    optimised_hues = solution.x
    
    fill = lambda H: [(h, S, L) for h in H]

    ResultTuple = namedtuple('ColourOptimiseResult', ['original', 'optimised'])
    return ResultTuple(fill(optimised_hues), fill(initial_hues))

def to_rgb(C):
    return C.rgb_r, C.rgb_g, C.rgb_b

def rgb_set(H):
    return [to_rgb(convert_color(HSLColor(h, s, v), sRGBColor)) for h, s, v in H]

def plot_palette(H, xaxis=None):
    import numpy as np
    import matplotlib.pyplot as plt
    
    width = 1
    height1 = np.ones(len(H))

    fig = plt.figure()

    if xaxis is None:
        xaxis = [i for i in range(len(H))]
        plt_ax = False
    else:
        plt_ax = True

    plt.bar(xaxis, height1, width=width, 
            color=[to_rgb(convert_color(hsv, sRGBColor)) for hsv in H])
    plt.xticks(rotation=90)

    if not plt_ax:
        ax = plt.gca()
        ax.axis('off')

    plt.show()
    return fig


def hsl_to_rgbh(HSLset):
    return [convert_color(HSLColor(h,s,l), sRGBColor).get_rgb_hex().upper() for h,s,l in HSLset]

def generate_palette_config(num_colours):
    # Generate a palette of n colours, and print to stdout

    import sys
    import configparser

    h0, hs = generate_palette(num_colours)

    #original_hex_strs = hsl_to_rgbh(h0)
    optimised_hex_strs = hsl_to_rgbh(hs)

    config = configparser.ConfigParser()
    config.optionxform = str
    config['Colours'] = {f'colour{i}':hx for i, hx in enumerate(optimised_hex_strs)}

    return config

def load_palette_config(ini_filename):
    # Load config lines as as place, (h, s, v)

    import configparser
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini_filename)

    places = []
    hex_strs = []
    for place, hex_str in config['Colours'].items():
        places.append(place)
        hex_strs.append(hex_str)

    HSLs = [convert_color(sRGBColor.new_from_rgb_hex(hex_str), HSLColor) for hex_str in hex_strs]
    
    return places, HSLs

def save_palette_single(ini_filename, output_filename='palette.png'):
    places, HSLs = load_palette_config(ini_filename)

    ## Sort HSLs, places by hue
    hsls = sorted(zip([h.get_value_tuple()[0] for h in HSLs], [i for i in range(len(HSLs))], places))
    _, inds, places = list(zip(*hsls))

    HSLs = [HSLs[i] for i in inds]

    fig = plot_palette(HSLs, xaxis=places)
    fig.savefig(output_filename)


help = '''usage: colours.py (NUM_COLOURS|names_file|palette_file [palette.png])

                If argument is ...
NUM_COLOURS     Integer - generate a list of palette colours.
names_file      File containing names list - generate an ini file. Name rows have duplicate colours.
ini_file        Ini containing palette - Plot and save palette to file.

                Generation times
10 colours < 10 seconds
40 colours < 10 mins
'''

if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) <= 1:
        print(help)
        exit(128)

    try:
        argument = sys.argv[1]

        if os.path.exists(argument):

            if '.ini' in argument:
                if len(sys.argv) >= 3:
                    png_file = sys.argv[2]
                else: 
                    png_file = 'palette.png'
                save_palette_single(argument, output_filename=png_file)
                exit(1)

            # Load list of names, each line as tuple
            with open(argument, 'r') as names_file:
                names = [N.split(' ') for N in names_file.readlines() if N]
                names = [[n.strip('\n') for n in N if n] for N in names]
        
            num_colours = len(names)

        else:
            try:
                num_colours = int(argument)
            except:
                print(help)
                exit(1)

        config = generate_palette_config(num_colours)
        if os.path.exists(argument):
            for i, (k, v) in enumerate(config['Colours'].items()):
                for name in names[i]:
                    config['Colours'][name] = v
                config.remove_option('Colours', k)

        config.write(sys.stdout)
        exit(0)
    except KeyboardInterrupt:
        exit(2)

    print(help)





