import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import ConnectionPatch

# Define the transformations
def clarke_transform(i_a, i_b, i_c):
    i_alpha = 2 / 3 * (i_a - 1 / 2 * i_b - 1 / 2 * i_c)
    i_beta = 2 / 3 * (np.sqrt(3) / 2 * i_b - np.sqrt(3) / 2 * i_c)
    return i_alpha, i_beta

def park_transform(i_a, i_b, i_c, theta):
    i_alpha, i_beta = clarke_transform(i_a, i_b, i_c)
    i_d = i_alpha * np.cos(theta) + i_beta * np.sin(theta)
    i_q = -i_alpha * np.sin(theta) + i_beta * np.cos(theta)
    return i_d, i_q

#set global font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 13})


# Parameters
n_frames = 180
angles = np.linspace(0, 2 * np.pi, n_frames)
i_a = np.sin(angles + np.pi / 2)
i_b = np.sin(angles - 2 * np.pi / 3 + np.pi / 2)
i_c = np.sin(angles + 2 * np.pi / 3 + np.pi / 2)
ahl = 0.1 # Arrow head length
deg_dq = np.pi/6 # Angle between d axis and rotating signal

# Generate the transformations for each frame
clarke_transforms = [clarke_transform(i_a[i], i_b[i], i_c[i]) for i in range(n_frames)]
park_transforms = [park_transform(i_a[i], i_b[i], i_c[i], angles[i] + deg_dq) for i in range(n_frames)]

#calculate the dq signals for each frame
ids, iqs = zip(*park_transforms)
ialpha, ibetas = zip(*clarke_transforms)

# 3x2 grid of plots with first column being quadraticly sized and second column have 3x the width of the first column
fig, axes = plt.subplots(3, 2, figsize=(16, 9), gridspec_kw={'width_ratios': [3, 9]})
fig.tight_layout(pad=3.0)
plt.subplots_adjust(wspace=0.01)

def add_horizontal_lines(ax_from, ax_to):
    ax_to.add_artist(ConnectionPatch(
        xyA=(-1, 1), xyB=(2 * np.pi, 1),
        coordsA="data", coordsB="data",
        axesA=ax_from, axesB=ax_to,
        color="black", linestyle="--"
    ))
    ax_to.add_artist(ConnectionPatch(
        xyA=(-1, -1), xyB=(2 * np.pi, -1),
        coordsA="data", coordsB="data",
        axesA=ax_from, axesB=ax_to,
        color="black", linestyle="--"
    ))


def update_plot(i):
    for ax in axes.flat:
        ax.clear()

    theta = angles[i]

    # Top left: abc phasor
    axes[0, 0].arrow(-1, 0, 2, 0, head_width=0.05, head_length=0.1, fc='k', ec='k', length_includes_head=True)
    axes[0, 0].arrow(1/2, -np.sqrt(3)/2, -1, np.sqrt(3), head_width=0.05, head_length=0.1, fc='k', ec='k', length_includes_head=True)
    axes[0, 0].arrow(1/2, np.sqrt(3)/2, -1, -np.sqrt(3), head_width=0.05, head_length=0.1, fc='k', ec='k', lw=1, length_includes_head=True)
    axes[0, 0].set_xlim(-1.1, 1.1)
    axes[0, 0].set_ylim(-1.1, 1.1)
    axes[0, 0].arrow(0, 0, np.cos(theta),  np.sin(theta), head_width=0.05, head_length=ahl, fc='m', ec='m', length_includes_head=True)
    axes[0, 0].arrow(0, 0, i_a[i] * 2 / 3, 0, head_width=0.05, head_length=ahl * 2 /3 , fc='r', ec='r' , length_includes_head=True)
    axes[0, 0].arrow(i_a[i]* 2 / 3, 0, i_b[i] * np.cos(2 / 3 * np.pi) * 2 / 3, i_b[i] * np.sin(2 / 3 * np.pi) * 2 / 3, head_width=0.05, head_length=ahl * 2 /3, fc='b', ec='b', length_includes_head=True)
    axes[0, 0].arrow((i_a[i] + i_b[i] * np.cos(2 / 3 * np.pi)) * 2 / 3, i_b[i] * np.sin(2 / 3 * np.pi) * 2 / 3, i_c[i] * np.cos(4 / 3 * np.pi) * 2 / 3, i_c[i] * np.sin(4 / 3 * np.pi) * 2 / 3, head_width=0.05, head_length=ahl * 2 /3, fc='g', ec='g', length_includes_head=True)
    axes[0, 0].text(1.1, 0, 'a', fontsize=12, va='center')
    axes[0, 0].text(-1/2 - 0.18, np.sqrt(3)/2 + 0.025, 'b', fontsize=12, va='center')
    axes[0, 0].text(-1/2 - 0.18, -np.sqrt(3)/2 - 0.05, 'c', fontsize=12, va='center')
    circle = plt.Circle((0, 0), 1, color='black', fill=False, lw=1)
    axes[0, 0].add_artist(circle)
    axes[0, 0].set_aspect('equal')

    # Top right: abc signals
    axes[0, 1].plot(angles, i_a, 'r')
    axes[0, 1].plot(angles, i_b, 'b')
    axes[0, 1].plot(angles, i_c, 'g')
    axes[0, 1].set_xlim(0, 2 * np.pi)
    axes[0, 1].set_ylim(-1.1, 1.1)
    axes[0, 1].set_ylabel(r'$x_\mathrm{abc}$')
    axes[0, 1].set_title('abc signals')
    axes[0, 1].axvline(x=theta, color='m', linestyle='--')
    axes[0, 1].scatter(theta, i_a[i], color='r', marker='o')
    axes[0, 1].scatter(theta, i_b[i], color='b', marker='o')
    axes[0, 1].scatter(theta, i_c[i], color='g', marker='o')
    axes[0, 1].set_xticks([0, np.pi/2, np.pi, 3/2*np.pi, 2*np.pi])
    axes[0, 1].set_xticklabels([r'0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    axes[0, 1].set_xlabel(r'$\varepsilon$')
    axes[0, 1].grid(True)
    add_horizontal_lines(axes[0, 0], axes[0, 1])
    axes[0, 1].get_yaxis().set_visible(False)
    axes[0, 0].get_yaxis().set_visible(True)
    axes[0, 0].get_xaxis().set_visible(False)
    axes[0, 0].spines['top'].set_visible(False)
    axes[0, 0].spines['right'].set_visible(False)
    axes[0, 0].spines['bottom'].set_visible(False)
    axes[0, 0].set_yticks([-1, -0.5, 0, 0.5, 1])
    axes[0, 1].axhline(y=0, color='black', linestyle='--', lw=1)

    # Middle left: alpha-beta phasor
    axes[1, 0].arrow(-1, 0, 2, 0, head_width=0.05, head_length=0.1, fc='k', ec='k', length_includes_head=True)
    axes[1, 0].arrow(0, -1, 0, 2, head_width=0.05, head_length=0.1, fc='k', ec='k', length_includes_head=True)
    axes[1, 0].arrow(0, 0, np.cos(theta),  np.sin(theta), head_width=0.05, head_length=ahl, fc='m', ec='m', length_includes_head=True)
    axes[1, 0].arrow(0, 0, clarke_transform(i_a[i], i_b[i], i_c[i])[0] , 0, head_width=0.05, head_length=ahl , fc='r', ec='r' , length_includes_head=True)
    axes[1, 0].arrow(clarke_transform(i_a[i], i_b[i], i_c[i])[0], 0,  0, clarke_transform(i_a[i], i_b[i], i_c[i])[1], head_width=0.05, head_length=ahl , fc='b', ec='b' , length_includes_head=True)
    axes[1, 0].set_xlim(-1.1, 1.1)
    axes[1, 0].set_ylim(-1.1, 1.1)
    axes[1, 0].text(1.1, 0, r'$\alpha$', fontsize=12, va='center')
    axes[1, 0].text(0, 1.15, r'$\beta$', fontsize=12, va='center', ha='center')
    circle = plt.Circle((0, 0), 1, color='black', fill=False, lw=1)
    axes[1, 0].add_artist(circle)
    axes[1, 0].set_aspect('equal')
    axes[1, 0].spines['top'].set_visible(False)
    axes[1, 0].spines['right'].set_visible(False)
    axes[1, 0].spines['bottom'].set_visible(False)
    axes[1, 0].set_yticks([-1, -0.5, 0, 0.5, 1])
    axes[1, 1].get_yaxis().set_visible(False)
    axes[1, 0].get_yaxis().set_visible(True)
    axes[1, 0].get_xaxis().set_visible(False)

    # Middle right: alpha-beta signals
    axes[1, 1].plot(angles, clarke_transform(i_a[:], i_b[:], i_c[:])[0], 'r')
    axes[1, 1].plot(angles, clarke_transform(i_a[:], i_b[:], i_c[:])[1], 'b')
    axes[1, 1].set_xlim(0, 2 * np.pi)
    axes[1, 1].set_ylim(-1.1, 1.1)
    axes[1, 1].set_ylabel(r'$x_\mathrm{abc}$')
    axes[1, 1].set_title(r'$\alpha\beta$ signals')
    axes[1, 1].set_xticks([0, np.pi/2, np.pi, 3/2*np.pi, 2*np.pi])
    axes[1, 1].set_xticklabels([r'0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    axes[1, 1].set_xlabel(r'$\varepsilon$')
    axes[1, 1].grid(True)
    axes[1, 1].axhline(y=0, color='black', linestyle='--', lw=1)
    add_horizontal_lines(axes[1, 0], axes[1, 1])
    axes[1, 1].axvline(x=theta, color='m', linestyle='--')
    axes[1, 1].scatter(theta, clarke_transform(i_a[i], i_b[i], i_c[i])[0], color='r', marker='o')
    axes[1, 1].scatter(theta, clarke_transform(i_a[i], i_b[i], i_c[i])[1], color='b', marker='o')


    # Bottom left: dq phasor
    axes[2, 0].arrow(-np.cos(theta + deg_dq), -np.sin(theta + deg_dq), 2 * np.cos(theta + deg_dq),  2 * np.sin(theta + deg_dq), head_width=0.05, head_length=ahl, fc='k', ec='k', length_includes_head=True)
    axes[2, 0].arrow(-np.cos(theta + deg_dq + np.pi / 2), -np.sin(theta + deg_dq + np.pi / 2), 2 * np.cos(theta + deg_dq + np.pi / 2),  2 * np.sin(theta + deg_dq + np.pi / 2), head_width=0.05, head_length=ahl, fc='k', ec='k', length_includes_head=True)
    axes[2, 0].arrow(0, 0, np.cos(theta),  np.sin(theta), head_width=0.05, head_length=ahl, fc='m', ec='m', length_includes_head=True)
    axes[2, 0].arrow(0, 0, park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[0] * np.cos(theta + deg_dq) , park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[0] * np.sin(theta + deg_dq), head_width=0.05, head_length=ahl , fc='r', ec='r' , length_includes_head=True)
    axes[2, 0].arrow(park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[0] * np.cos(theta + deg_dq) , park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[0] * np.sin(theta + deg_dq),  park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[1] * np.cos(theta + deg_dq + np.pi / 2), park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[1] * np.sin(theta + deg_dq + np.pi / 2) , head_width=0.05, head_length=ahl , fc='b', ec='b' , length_includes_head=True)
    axes[2, 0].set_xlim(-1.1, 1.1)
    axes[2, 0].set_ylim(-1.1, 1.1)
    axes[2, 0].spines['top'].set_visible(False)
    axes[2, 0].spines['right'].set_visible(False)
    axes[2, 0].spines['bottom'].set_visible(False)
    axes[2, 0].get_yaxis().set_visible(True)
    axes[2, 0].get_xaxis().set_visible(False)
    axes[2, 0].set_yticks([-1, -0.5, 0, 0.5, 1])
    circle = plt.Circle((0, 0), 1, color='black', fill=False, lw=1)
    axes[2, 0].add_artist(circle)
    axes[2, 0].set_aspect('equal')
    axes[2, 0].text(np.cos(theta + deg_dq) * 1.15, np.sin(theta + deg_dq) * 1.15, 'd', fontsize=12, va='center', ha='center')
    axes[2, 0].text(np.cos(theta + deg_dq + np.pi /2) * 1.15, np.sin(theta + deg_dq + np.pi /2) * 1.15, 'q', fontsize=12, va='center', ha='center')

    # Bottom right: dq signals
    axes[2, 1].plot(angles,  ids, 'b')
    axes[2, 1].plot(angles,  iqs, 'r')
    axes[2, 1].set_xlim(0, 2 * np.pi)
    axes[2, 1].set_ylim(-1.1, 1.1)
    axes[2, 1].set_ylabel(r'$x_\mathrm{dq}$')
    axes[2, 1].set_title('dq signals')
    axes[2, 1].set_xticks([0, np.pi/2, np.pi, 3/2*np.pi, 2*np.pi])
    axes[2, 1].set_xticklabels([r'0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    axes[2, 1].set_xlabel(r'$\varepsilon$')
    axes[2, 1].grid(True)
    axes[2, 1].axhline(y=0, color='black', linestyle='--', lw=1)
    axes[2, 1].axvline(x=theta, color='m', linestyle='--')
    axes[2, 1].scatter(theta, park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[0], color='b', marker='o')
    axes[2, 1].scatter(theta, park_transform(i_a[i], i_b[i], i_c[i], theta+deg_dq)[1], color='r', marker='o')
    add_horizontal_lines(axes[2, 0], axes[2, 1])
    axes[2, 1].axhline(y=0, color='black', linestyle='--', lw=1)
    axes[2, 1].get_yaxis().set_visible(False)

update_plot(20)
plt.show()

# Create the animation
ani = animation.FuncAnimation(fig, update_plot, frames=n_frames, repeat=True)
ani.save('Clarke_Park.gif', writer='imagemagick', fps=30)
plt.show()
