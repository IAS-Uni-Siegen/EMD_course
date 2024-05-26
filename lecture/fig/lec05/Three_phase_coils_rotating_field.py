"""
Demonstration of rotating field in a three-phase system

Based (but heavily modified) on the following code:
https://perso.univ-lyon1.fr/charles.joubert/web_anim/simen_rotfield_create.html
Initial work from Josh Lifton
Intermediate update from Charles Joubert
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import math
from PIL import Image

plt.rcParams['text.usetex'] = True

# Background image filename
BKG_FILENAME = 'Three_phase_coils_rotating_field_background.png'

# Argument parser
epilog = """
Examples

GIF output. The only powered coil is coil 1:
Python Three_phase_coils_rotating_field.py -g -1

GIF output. All coils are powered. The resulting field is also plotted and saved as a .gif file:
Python Three_phase_coils_rotating_field.py -g --all -c -r -o Three_phase_coils_rotating_field
"""

parser = argparse.ArgumentParser(description='Create animation of rotating field', epilog=epilog,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-1', '--coil1', action='store_true', help='plot coil 1 field')
parser.add_argument('-2', '--coil2', action='store_true', help='plot coil 2 field')
parser.add_argument('-3', '--coil3', action='store_true', help='plot coil 3 field')
parser.add_argument('-A', '--all', action='store_true', help='plot all 3 fields')
parser.add_argument('-c', '--compose', action='store_true', help='vectors are plotted "chained"')
parser.add_argument('-r', '--resulting', action='store_true', help='draw resulting magnetic field in black')
parser.add_argument('-m', '--compass-angle', type=int, default=None, help='draw a compass with given angle shift. Default: no compass drawn')
parser.add_argument('-p', '--preserve', action='store_true', help='do not delete individual PartialOut*.png files')
parser.add_argument('--fps', type=int, default=10, help='frames per second')
parser.add_argument('-f', '--frames', type=int, default=50, help='total number of frames')
parser.add_argument('-o', '--output', default='output_file', help='output file (without extension)')
parser.add_argument('-g', '--gif', action='store_true', help='outputs .gif file')

args = parser.parse_args()

# Configuration
OUT_FILENAME = args.output # Output filename (without extension)
GIF_OUTPUT = args.gif # Boolean indicating if GIF output is required
NUMBER_OF_TIME_STEPS = args.frames # Total number of frames
FPS = args.fps # Frames per second
D = 0.001 # Margin between figures
W1 = 0.25 # Width of sinusoidal figures
H1 = 0.95 * (1 - 4 * D) / 3 # Height of sinusoidal figures
CENTERFIG = (614, 763) # Coordinates of the center of the figure (for rotating field vectors)
VL = 135 # Vector length 
VHL = 45 # Vector arrow size
DRAWV = [args.coil1, args.coil2, args.coil3] if not args.all else [True, True, True] # Which coils to plot
COMPOSE = args.compose # If vectors are plotted "chained"
DRAWRES = args.resulting # If resulting field is also plotted
ANGLE_BOUSSOLE = -args.compass_angle if args.compass_angle is not None else None
DRAW_ARROWS = True # If arrows are drawn
PHASES = ['a', 'b', 'c'] # Define phase names

# Function to draw a triangle
def draw_triangle(ax, angle, color="red", size=20):
    points = [(0, -size), (2 * size, 0), (0, +size)]
    angle = -angle
    p_tr = [(p[0] * math.cos(angle) - p[1] * math.sin(angle) + CENTERFIG[0],
             p[0] * math.sin(angle) + p[1] * math.cos(angle) + CENTERFIG[1]) for p in points]
    p = mpatches.Polygon(p_tr, closed=True, fill=True, color="k", fc=color)
    ax.add_patch(p)

# Main plotting loop # List to store filenames of generated frames
filenames = []

for i in range(NUMBER_OF_TIME_STEPS):
    fig = plt.figure() # Create a new figure
    fig.set_facecolor('w') # Set figure background color to white
    img = mpimg.imread(BKG_FILENAME)  # Load background image
    
    # Create axes for the sinusoidal plots
    axp = [fig.add_axes([D, k * ((1 - 4 * D) / 3 + D) + D, W1, H1]) for k in range(3)]
    styles = ['r', 'b', 'g'] # Colors for the coils
    axi = fig.add_axes([W1 + 2 * D, D, 1 - 3 * D - W1, 1 - 2 * D]) # Main axes
    axi.set_axis_off() # Turn off axis lines and labels


    x1, y1 = CENTERFIG # Initialize vector start point at the center

    for j, ax in enumerate(axp):
        # Plot axes and labels
        ax.arrow(0, 0, 2 * np.pi*0.98, 0, head_width=0.1, head_length=0.2, fc='k', ec='k')   
        ax.arrow(0, -1, 0, 2*0.98, head_width=0.3, head_length=0.1, fc='k', ec='k',)
        ax.text(2 * np.pi, -0.35, r'$t$', color='k', fontsize=16)
        ax.text(-1, 1, r'$i_\mathrm{' + PHASES[j] + '}$', color=styles[j], fontsize=16)
        fig.sca(ax)
        y = np.cos(np.linspace(0, 2 * np.pi, 500) - j * 2 * np.pi / 3) # Sinusoidal wave for each coil
        xp = i * 2 * np.pi / NUMBER_OF_TIME_STEPS # Current x position on the wave
        yp = np.cos(xp - j * 2 * np.pi / 3) # Current y position on the wave
        if DRAWV[j]:
            # Plot the wave and current point
            plt.plot(np.linspace(0, 2 * np.pi, 500), y, styles[j] + '-', xp, yp, styles[j] + 'o')
            fig.sca(axi)
            dx = VL * yp * np.cos(j * 2 * np.pi / 3) # Change in x for the vector
            dy = VL * yp * np.sin(-j * 2 * np.pi / 3) # Change in y for the vector
            if DRAW_ARROWS:
                plt.arrow(x1, y1, dx, dy, color=styles[j], head_width=VHL, head_length=VHL)
            if COMPOSE:
                x1 += (VL * yp) * np.cos(j * 2 * np.pi / 3) + np.sign(yp) * VHL * np.cos(j * 2 * np.pi / 3)
                y1 += (VL * yp) * np.sin(-j * 2 * np.pi / 3) + np.sign(yp) * VHL * np.sin(-j * 2 * np.pi / 3)
        ax.set_xlim(-1.1, 2 * np.pi + 0.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_axis_off()

    if ANGLE_BOUSSOLE is not None:
        # Draw compass if angle is specified
        a = ANGLE_BOUSSOLE * np.pi / 180 + i * 2 * np.pi / NUMBER_OF_TIME_STEPS
        draw_triangle(axi, a)
        draw_triangle(axi, a + np.pi, color="white")

    if DRAWRES:
        # Draw the resulting field vector
        plt.arrow(CENTERFIG[0], CENTERFIG[1], x1 - CENTERFIG[0] - np.sign(yp) * VHL * np.cos(j * 2 * np.pi / 3), y1 - CENTERFIG[1] - np.sign(yp) * VHL * np.sin(-j * 2 * np.pi / 3), color='k', head_width=VHL, head_length=VHL, linewidth=2, alpha=0.5)

    fig.sca(axi)
    plt.imshow(img) # Display the background image

    if GIF_OUTPUT:
        filename = f'PartialOut{i:03d}.png'
        plt.savefig(filename, dpi=320) # Save the frame as a PNG file
        filenames.append(filename) # Add the filename to the list

    plt.close(fig) # Close the figure to free up memory

if GIF_OUTPUT:
    # Create GIF using Pillow
    images = [Image.open(filename) for filename in filenames]
    images[0].save(f'{OUT_FILENAME}.gif', save_all=True, append_images=images[1:], duration=1000//FPS, loop=0)
    print(f"\n\n The movie was written to '{OUT_FILENAME}.gif'")

if GIF_OUTPUT and not args.preserve:
    # Delete temporary PNG files if preserve option is not set
    print("Deleting temporary .png files...")
    for filename in filenames:
        os.unlink(filename)
