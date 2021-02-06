import matplotlib
import random

def colors():

    hex_colors = []
    for name, hex in matplotlib.colors.cnames.items():
        hex_colors.append(hex)

    return hex_colors

def random_colors(nbr_colors):
    return random.choices(colors(), k=nbr_colors)
