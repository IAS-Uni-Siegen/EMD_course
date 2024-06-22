import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#set global font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 13})

# Frequency parameters (assuming induction machine with a single pole pair)
omega_me = 50 * 2* np.pi # mechanical rotor speed
slip = 0 # slip
omega_r = omega_me / (1 - slip) # electrical frequency of the stator currents
omega_s = omega_r + omega_me # electrical frequency of the rotor currents
phi = -np.pi / 2 # load angle

# Plotting parameters
radius_coil = 0.1
max_marker_size_X = 15
max_marker_size_circle = 0.04
radius_rotor_slot = 0.6
radius_air_gap = radius_rotor_slot + radius_coil + 0.1

# Definition of basic rotor slot positions for eps_me = 0
rotor_a_pos = np.array([0, 1]) * radius_rotor_slot
rotor_a_neg = np.array([0, -1]) * radius_rotor_slot
rotor_b_pos = np.array([np.sqrt(3)/2, 0.5]) *radius_rotor_slot
rotor_b_neg = np.array([-np.sqrt(3)/2, -0.5]) * radius_rotor_slot
rotor_c_pos = np.array([-np.sqrt(3)/2, 0.5]) * radius_rotor_slot
rotor_c_neg = np.array([np.sqrt(3)/2, -0.5]) * radius_rotor_slot

# Animation parameters
n_frames = 300
t_vec = np.linspace(0, 2*np.pi / np.abs(np.min([omega_s, omega_me])), n_frames)
theta_vec = np.linspace(0, 2*np.pi, n_frames)

# Stator currents
i_sa = np.cos(omega_s * t_vec)
i_sb = np.cos(omega_s * t_vec - 2*np.pi/3)
i_sc = np.cos(omega_s * t_vec - 4*np.pi/3)

# Rotor currents
i_ra = np.cos(omega_r * t_vec + phi)
i_rb = np.cos(omega_r * t_vec - 2*np.pi/3 + phi)
i_rc = np.cos(omega_r * t_vec + 2*np.pi/3 + phi)

fig, ax = plt.subplot_mosaic(
    [
        ['isa', 'motor', 'ira'],
        ['isb', 'motor', 'irb'],
        ['isc', 'motor', 'irc'],
    ],
    width_ratios=[1, 1, 1],
    layout='constrained',
    figsize=(16, 9)
)
fig.tight_layout(pad=3.0)
plt.subplots_adjust(wspace=0.01)

def update_plot(i):
    # clear all subplots
    for key in ax.keys():
        ax[key].cla()

    t = t_vec[i]    

    # 2D rotations matrix (math positive) - Park transform
    Tp = np.array([[np.cos(omega_me * t), -np.sin(omega_me * t)], [np.sin(omega_me * t), np.cos(omega_me * t)]])

    # Fundamental component of the stator B field
    B_hat = 1
    B = B_hat * np.cos(omega_s * t - theta_vec)

    # Calculate the rotor position and rotor slot angles for the current time step
    eps_me = omega_me * t
    eps_me_ra_pos = eps_me + np.pi / 2
    eps_me_ra_neg = eps_me - np.pi / 2
    eps_me_rb_pos = eps_me + 2 * np.pi / 3 + np.pi / 2
    eps_me_rb_neg = eps_me + np.pi / 6
    eps_me_rc_pos = eps_me - np.pi / 6
    eps_me_rc_neg = eps_me + np.pi * 5 / 6

   
    # Calculate the absolute Lorentz force acting on the rotor coils
    F_ra_pos = B_hat * np.cos(omega_s * t - eps_me_ra_pos) * i_ra[i]
    F_ra_neg = B_hat * np.cos(omega_s * t - eps_me_ra_neg) * i_ra[i]
    F_rb_pos = B_hat * np.cos(omega_s * t - eps_me_rb_pos) * i_rb[i]
    F_rb_neg = B_hat * np.cos(omega_s * t - eps_me_rb_neg) * i_rb[i]
    F_rc_pos = B_hat * np.cos(omega_s * t - eps_me_rc_pos) * i_rc[i]
    F_rc_neg = B_hat * np.cos(omega_s * t - eps_me_rc_neg) * i_rc[i]
    

    #Remove all axis labels from 'motor' subplot
    ax['motor'].axis('off')

    # plot stator currents
    ax['isa'].plot(t_vec, i_sa, color='red')
    ax['isb'].plot(t_vec, i_sb, color='blue')
    ax['isc'].plot(t_vec, i_sc, color='green')

    # add vertical lines and markers to indicate the current time step for stator currents
    ax['isa'].axvline(t, color='black', linestyle='--')
    ax['isb'].axvline(t, color='black', linestyle='--')
    ax['isc'].axvline(t, color='black', linestyle='--')
    ax['isa'].plot(t, i_sa[i], 'ro')
    ax['isb'].plot(t, i_sb[i], 'bo')
    ax['isc'].plot(t, i_sc[i], 'go')

    # add y-axis labels is/ismax LaTeX labels to stator current subplots
    ax['isa'].set_ylabel(r'$i_{\mathrm{s,a}}(t)/i_{\mathrm{s,max}}$')
    ax['isb'].set_ylabel(r'$i_{\mathrm{s,b}}(t)/i_{\mathrm{s,max}}$')
    ax['isc'].set_ylabel(r'$i_{\mathrm{s,c}}(t)/i_{\mathrm{s,max}}$')

    # plot rotor currents with y-axis labels and y ticks to the right
    ax['ira'].plot(t_vec, i_ra, color='red')
    ax['irb'].plot(t_vec, i_rb, color='blue')
    ax['irc'].plot(t_vec, i_rc, color='green')

    # add y-axis labels ir/irmax LaTeX labels to rotor current subplots
    ax['ira'].set_ylabel(r'$i_{\mathrm{r,a}}(t)/i_{\mathrm{r,max}}$')
    ax['irb'].set_ylabel(r'$i_{\mathrm{r,b}}(t)/i_{\mathrm{r,max}}$')
    ax['irc'].set_ylabel(r'$i_{\mathrm{r,c}}(t)/i_{\mathrm{r,max}}$')

     # add vertical lines and markers to indicate the current time step for rotor currents
    ax['ira'].axvline(t, color='black', linestyle='--')
    ax['irb'].axvline(t, color='black', linestyle='--')
    ax['irc'].axvline(t, color='black', linestyle='--')
    ax['ira'].plot(t, i_ra[i], 'ro')
    ax['irb'].plot(t, i_rb[i], 'bo')
    ax['irc'].plot(t, i_rc[i], 'go')

    # add x-axis label to the last row of subplots
    ax['isc'].set_xlabel(r'$t$ in s')
    ax['irc'].set_xlabel(r'$t$ in s')

  


    
 
    # shift y-axis labels to the right of the subplots
    for key in ax.keys():
        # search for keys starting with 'ir' 
        if key.startswith('ir'):
            ax[key].yaxis.set_label_position('right')
            ax[key].yaxis.tick_right()

    # increase the plot widht to the right of the subplots such that the y-axis labels are not cut off
    fig.subplots_adjust(right=0.95)

    # add background grid to all subplots except 'motor' and set x-limits to min/max in t_vec
    for key in ax.keys():
        if key != 'motor':
            ax[key].grid(True)
            ax[key].set_xlim([np.min(t_vec), np.max(t_vec)])
            ax[key].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.3f}'.format(x)))



    # Plot a circle at (x=0, y=1) with radius 0.1 and a red border (Phase A upper coil)
    circle = plt.Circle((0, 1), radius_coil, color='red', fill=False)
    ax['motor'].add_artist(circle)

      # Plot a circle at (x=0, y=-1) with radius 0.1 and a red border (Phase A lower coil)
    circle = plt.Circle((0, -1), radius_coil, color='red', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at (x=0, y=1) with max radius scaled by the stator current (if positive) or a X with max radius scaled by the stator current (if negative)
    # plot filled circle at (x=0, y=-1) with max radius scaled by the stator current (if negative) or a X with max radius scaled by the stator current (if positive)
    if i_sa[i] > 0:
        circle = plt.Circle((0, 1), max_marker_size_circle * i_sa[i], color='red', fill=True)
        ax['motor'].plot(0, -1, 'x', markersize = max_marker_size_X * np.abs(i_sa[i]), color='red')
    else:
        ax['motor'].plot(0, 1, 'x', markersize = max_marker_size_X * np.abs(i_sa[i]), color='red')
        circle = plt.Circle((0, -1), max_marker_size_circle * i_sa[i], color='red', fill=True)
    ax['motor'].add_artist(circle)
    

    # Plot two circles 120 ° shifted from the first two circles with blue border  (Phase B upper coil)
    circle = plt.Circle((np.sqrt(3)/2, 0.5), radius_coil, color='blue', fill=False)
    ax['motor'].add_artist(circle)

    # Plot two circles 120 ° shifted from the first two circles with blue border  (Phase B lower coil)
    circle = plt.Circle((-np.sqrt(3)/2, -0.5), radius_coil, color='blue', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at (np.sqrt(3)/2, 0.5) with max radius scaled by the stator current (if positive) or a X with max radius scaled by the stator current (if negative)
    # plot filled circle at (-np.sqrt(3)/2, -0.5) with max radius scaled by the stator current (if negative) or a X with max radius scaled by the stator current (if positive)
    if i_sb[i] > 0:
        ax['motor'].plot(np.sqrt(3)/2, 0.5, 'x', markersize = max_marker_size_X * np.abs(i_sb[i]), color='blue')
        circle = plt.Circle((-np.sqrt(3)/2, -0.5), max_marker_size_circle * i_sb[i], color='blue', fill=True)
    else:
        circle = plt.Circle((np.sqrt(3)/2, 0.5), max_marker_size_circle * i_sb[i], color='blue', fill=True)
        ax['motor'].plot(-np.sqrt(3)/2, -0.5, 'x', markersize = max_marker_size_X * np.abs(i_sb[i]), color='blue')
        
    ax['motor'].add_artist(circle)

    # Plot two circles 120 ° shifted from the first two circles with green border  (Phase C upper coil)
    circle = plt.Circle((-np.sqrt(3)/2, 0.5), radius_coil, color='green', fill=False)
    ax['motor'].add_artist(circle)

    # Plot two circles 120 ° shifted from the first two circles with green border  (Phase C lower coil)
    circle = plt.Circle((np.sqrt(3)/2, -0.5), radius_coil, color='green', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at (-np.sqrt(3)/2, 0.5) with max radius scaled by the stator current (if positive) or a X with max radius scaled by the stator current (if negative)
    # plot filled circle at (np.sqrt(3)/2, -0.5) with max radius scaled by the stator current (if negative) or a X with max radius scaled by the stator current (if positive)
    if i_sc[i] > 0:
        ax['motor'].plot(-np.sqrt(3)/2, 0.5, 'x', markersize = max_marker_size_X * np.abs(i_sc[i]), color='green')
        circle = plt.Circle((np.sqrt(3)/2, -0.5), max_marker_size_circle * i_sc[i], color='green', fill=True)
    else:
        circle = plt.Circle((-np.sqrt(3)/2, 0.5), max_marker_size_circle * i_sc[i], color='green', fill=True)
        ax['motor'].plot(np.sqrt(3)/2, -0.5, 'x', markersize = max_marker_size_X * np.abs(i_sc[i]), color='green')
    ax['motor'].add_artist(circle)


    # add an outer black circle to represent the stator outside diameter
    circle = plt.Circle((0, 0), 1 + 1.5 * radius_coil, color='black', fill=False)
    ax['motor'].add_artist(circle)

    # add an inner black circle to represent the stator inside diameter
    circle = plt.Circle((0, 0), 1 - 1.5 * radius_coil, color='black', fill=False)
    ax['motor'].add_artist(circle)

    # add a black circle to represent the rotor outside diameter
    circle = plt.Circle((0, 0), 1 - 1.5 * radius_coil-0.1, color='black', fill=False)
    ax['motor'].add_artist(circle)

    # plot circle for phase A pos. coil at current position
    rotor_a_pos_rot = np.dot(Tp, rotor_a_pos)
    circle = plt.Circle((rotor_a_pos_rot[0], rotor_a_pos_rot[1]), radius_coil, color='red', fill=False)
    ax['motor'].add_artist(circle)

    # plot circle for phase A neg. coil at current position
    rotor_a_neg_rot = np.dot(Tp, rotor_a_neg)
    circle = plt.Circle((rotor_a_neg_rot[0], rotor_a_neg_rot[1]), radius_coil, color='red', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at for phase A pos. rotor coil at current position with max radius scaled by the rotor current (if positive) or a X with max radius scaled by the rotor current (if negative)
    # plot filled circle at for phase A neg. rotor coil at current position with max radius scaled by the rotor current (if negative) or a X with max radius scaled by the rotor current (if positive)
    if i_ra[i] > 0:
        circle = plt.Circle((rotor_a_pos_rot[0], rotor_a_pos_rot[1]), max_marker_size_circle * i_ra[i], color='red', fill=True)
        ax['motor'].plot(rotor_a_neg_rot[0], rotor_a_neg_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_ra[i]), color='red')
    else:
        ax['motor'].plot(rotor_a_pos_rot[0], rotor_a_pos_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_ra[i]), color='red')
        circle = plt.Circle((rotor_a_neg_rot[0], rotor_a_neg_rot[1]), max_marker_size_circle * i_ra[i], color='red', fill=True)
    ax['motor'].add_artist(circle)
    
    # plot circle for phase B pos. coil at current position
    rotor_b_pos_rot = np.dot(Tp, rotor_b_pos)
    circle = plt.Circle((rotor_b_pos_rot[0], rotor_b_pos_rot[1]), radius_coil, color='blue', fill=False)
    ax['motor'].add_artist(circle)

    # plot circle for phase B neg. coil at current position
    rotor_b_neg_rot = np.dot(Tp, rotor_b_neg)
    circle = plt.Circle((rotor_b_neg_rot[0], rotor_b_neg_rot[1]), radius_coil, color='blue', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at for phase B pos. rotor coil at current position with max radius scaled by the rotor current (if positive) or a X with max radius scaled by the rotor current (if negative)
    # plot filled circle at for phase B neg. rotor coil at current position with max radius scaled by the rotor current (if negative) or a X with max radius scaled by the rotor current (if positive)
    if i_rb[i] > 0:
        ax['motor'].plot(rotor_b_pos_rot[0], rotor_b_pos_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_rb[i]), color='blue')
        circle = plt.Circle((rotor_b_neg_rot[0], rotor_b_neg_rot[1]), max_marker_size_circle * i_rb[i], color='blue', fill=True)
    else:
        circle = plt.Circle((rotor_b_pos_rot[0], rotor_b_pos_rot[1]), max_marker_size_circle * i_rb[i], color='blue', fill=True)
        ax['motor'].plot(rotor_b_neg_rot[0], rotor_b_neg_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_rb[i]), color='blue')
        
    ax['motor'].add_artist(circle)

    # plot circle for phase C pos. coil at current position
    rotor_c_pos_rot = np.dot(Tp, rotor_c_pos)
    circle = plt.Circle((rotor_c_pos_rot[0], rotor_c_pos_rot[1]), radius_coil, color='green', fill=False)
    ax['motor'].add_artist(circle)

    # plot circle for phase C neg. coil at current position
    rotor_c_neg_rot = np.dot(Tp, rotor_c_neg)
    circle = plt.Circle((rotor_c_neg_rot[0], rotor_c_neg_rot[1]), radius_coil, color='green', fill=False)
    ax['motor'].add_artist(circle)

    # plot filled circle at for phase C pos. rotor coil at current position with max radius scaled by the rotor current (if positive) or a X with max radius scaled by the rotor current (if negative)
    # plot filled circle at for phase C neg. rotor coil at current position with max radius scaled by the rotor current (if negative) or a X with max radius scaled by the rotor current (if positive)
    if i_rc[i] > 0:
        ax['motor'].plot(rotor_c_pos_rot[0], rotor_c_pos_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_rc[i]), color='green')
        circle = plt.Circle((rotor_c_neg_rot[0], rotor_c_neg_rot[1]), max_marker_size_circle * i_rc[i], color='green', fill=True)
    else:
        circle = plt.Circle((rotor_c_pos_rot[0], rotor_c_pos_rot[1]), max_marker_size_circle * i_rc[i], color='green', fill=True)
        ax['motor'].plot(rotor_c_neg_rot[0], rotor_c_neg_rot[1], 'x', markersize = max_marker_size_X * np.abs(i_rc[i]), color='green')
    ax['motor'].add_artist(circle)


    
    # Plot the B field fundamental as a quiver plot with the starting points along the air gap and the direction of the arrows orthogonal to the air gap. The length of the arrows should be scaled by the B field strength - ensure that the number of arrows is not larger than 100
    n_arrows = 100
    idx = np.linspace(0, len(theta_vec)-1, n_arrows, dtype=int)
    for j in idx:
         B_handle = ax['motor'].quiver(np.cos(theta_vec[j]) * radius_air_gap - B[j]*np.cos(theta_vec[j])/6, np.sin(theta_vec[j]) * radius_air_gap - B[j]*np.sin(theta_vec[j])/6, B[j]*np.cos(theta_vec[j]), B[j]*np.sin(theta_vec[j]), color='gray', scale_units='xy', scale=3, width=0.005, label='B field')
    

    # Plot the Lorentz force acting on the rotor coils as a quiver plot with the starting points at the rotor coil positions and the direction of the arrows orthogonal to the rotor coil positions. The length of the arrows should be scaled by the Lorentz force acting on the rotor coils
    ax['motor'].quiver(rotor_a_pos_rot[0], rotor_a_pos_rot[1], -F_ra_pos*np.sin(eps_me_ra_pos), F_ra_pos*np.cos(eps_me_ra_pos), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    ax['motor'].quiver(rotor_a_neg_rot[0], rotor_a_neg_rot[1], F_ra_neg*np.sin(eps_me_ra_neg), -F_ra_neg*np.cos(eps_me_ra_neg), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    ax['motor'].quiver(rotor_b_pos_rot[0], rotor_b_pos_rot[1], F_rb_pos*np.sin(eps_me_rb_pos), -F_rb_pos*np.cos(eps_me_rb_pos), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    ax['motor'].quiver(rotor_b_neg_rot[0], rotor_b_neg_rot[1], -F_rb_neg*np.sin(eps_me_rb_neg), F_rb_neg*np.cos(eps_me_rb_neg), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    ax['motor'].quiver(rotor_c_pos_rot[0], rotor_c_pos_rot[1], F_rc_pos*np.sin(eps_me_rc_pos), -F_rc_pos*np.cos(eps_me_rc_pos), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_c_neg_rot[0], rotor_c_neg_rot[1], -F_rc_neg*np.sin(eps_me_rc_neg),  F_rc_neg * np.cos(eps_me_rc_neg), color='#7401d8ff', scale_units='xy', scale=3, width=0.005, label='Lorentz Force')

    

    # set motor subplot limits to -1.5 to 1.5 in both x and y directions
    ax['motor'].set_xlim(-1.5, 1.5)
    ax['motor'].set_ylim(-1.5, 1.5)

    # set motor subplot aspect ratio to be equal
    ax['motor'].set_aspect('equal')

    #set the legend entries vertically stacked over each other
    ax['motor'].legend((B_handle, force_handle), ('B field (stator normal component, fundamental)', 'Lorentz Force'), loc='lower center', ncol=1, fancybox=True, bbox_to_anchor=(0.5, -0.05))











#update_plot(0)
#plt.show()



ani = animation.FuncAnimation(fig, update_plot, frames=n_frames, repeat=True)
ani.save('IM_slip_0_load_angle_90_animation.gif', writer='imagemagick', fps=25)
plt.show()



