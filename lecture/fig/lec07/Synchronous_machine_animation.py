import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import os 

#set global font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 13})

# Frequency parameters (assuming synchronous machine with a single pole pair)
omega_me = 50 * 2* np.pi # mechanical rotor speed
omega_s = omega_me  # electrical frequency of the stator currents
phi = 0 * np.pi / 2 # load angle

# Plotting parameters
radius_coil = 0.1
max_marker_size_X = 15
max_marker_size_circle = 0.04
radius_rotor_slot = 0.6
radius_air_gap = radius_rotor_slot + radius_coil + 0.1

# Definition of basic rotor turn positions for eps_me = 0
rotor_pos_01 = np.array([-0.6, 0.6]) * radius_rotor_slot
rotor_pos_02 = np.array([-0.6, 0.2]) * radius_rotor_slot
rotor_pos_03 = np.array([-0.6, -0.2]) * radius_rotor_slot
rotor_pos_04 = np.array([-0.6, -0.6]) * radius_rotor_slot
rotor_neg_01 = np.array([0.6, 0.6]) * radius_rotor_slot
rotor_neg_02 = np.array([0.6, 0.2]) * radius_rotor_slot
rotor_neg_03 = np.array([0.6, -0.2]) * radius_rotor_slot
rotor_neg_04 = np.array([0.6, -0.6]) * radius_rotor_slot

rotor_salient_01 = np.array([-0.4, 0.85]) * radius_rotor_slot
rotor_salient_02 = np.array([-0.4, -0.85]) * radius_rotor_slot
rotor_salient_03 = np.array([0.4, 0.85]) * radius_rotor_slot
rotor_salient_04 = np.array([0.4, -0.85]) * radius_rotor_slot
rotor_salient_05 = np.array([0, 0.9]) * radius_rotor_slot
rotor_salient_06 = np.array([0, -0.9]) * radius_rotor_slot

# Animation parameters
n_frames = 300
t_vec = np.linspace(0, 2*np.pi / omega_s, n_frames)
theta_vec = np.linspace(0, 2*np.pi, n_frames)

# Stator currents
i_sa = np.cos(omega_s * t_vec)
i_sb = np.cos(omega_s * t_vec - 2*np.pi/3)
i_sc = np.cos(omega_s * t_vec - 4*np.pi/3)


fig, ax = plt.subplot_mosaic(
    [
        ['isa', 'ir'],
        ['isb', 'motor'],
        ['isc', 'motor'],
    ],
    width_ratios=[1, 1],
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
    eps = omega_s * t + phi + np.pi/2

    # 2D rotations matrix (math positive) - Park transform
    Tp = np.array([[np.cos(omega_me * t), -np.sin(omega_me * t)], [np.sin(omega_me * t), np.cos(omega_me * t)]])
    Tp_eps = np.array([[np.cos(eps), -np.sin(eps)], [np.sin(eps), np.cos(eps)]])

    # Fundamental component of the stator B field
    B_hat = 1
    B_theta_vec = omega_s * t - theta_vec
    
    # shift B_theta_vec angles towards 0...2*pi
    B_theta_vec = (B_theta_vec + 2*np.pi) % (2*np.pi)
    B = B_hat * np.cos(B_theta_vec)



    # Calculate the rotor position and rotor turn angles for the current time step
    rotor_pos_01_rot = np.dot(Tp_eps, rotor_pos_01)
    rotor_pos_02_rot = np.dot(Tp_eps, rotor_pos_02)
    rotor_pos_03_rot = np.dot(Tp_eps, rotor_pos_03)
    rotor_pos_04_rot = np.dot(Tp_eps, rotor_pos_04)
    rotor_neg_01_rot = np.dot(Tp_eps, rotor_neg_01)
    rotor_neg_02_rot = np.dot(Tp_eps, rotor_neg_02)
    rotor_neg_03_rot = np.dot(Tp_eps, rotor_neg_03)
    rotor_neg_04_rot = np.dot(Tp_eps, rotor_neg_04)

    rotor_salient_01_rot = np.dot(Tp_eps, rotor_salient_01)
    rotor_salient_02_rot = np.dot(Tp_eps, rotor_salient_02)
    rotor_salient_03_rot = np.dot(Tp_eps, rotor_salient_03)
    rotor_salient_04_rot = np.dot(Tp_eps, rotor_salient_04)
    rotor_salient_05_rot = np.dot(Tp_eps, rotor_salient_05)
    rotor_salient_06_rot = np.dot(Tp_eps, rotor_salient_06)

    # Calculate the rotor turn angles for the current time step
    eps_r_pos_01 = np.arctan2(rotor_pos_01_rot[1], rotor_pos_01_rot[0])
    eps_r_pos_02 = np.arctan2(rotor_pos_02_rot[1], rotor_pos_02_rot[0])
    eps_r_pos_03 = np.arctan2(rotor_pos_03_rot[1], rotor_pos_03_rot[0])
    eps_r_pos_04 = np.arctan2(rotor_pos_04_rot[1], rotor_pos_04_rot[0])
    eps_r_neg_01 = np.arctan2(rotor_neg_01_rot[1], rotor_neg_01_rot[0])
    eps_r_neg_02 = np.arctan2(rotor_neg_02_rot[1], rotor_neg_02_rot[0])
    eps_r_neg_03 = np.arctan2(rotor_neg_03_rot[1], rotor_neg_03_rot[0])
    eps_r_neg_04 = np.arctan2(rotor_neg_04_rot[1], rotor_neg_04_rot[0])

    # Map all rotor turn angles to 0...2*pi
    eps_r_pos_01 = (eps_r_pos_01 + 2*np.pi) % (2*np.pi)
    eps_r_pos_02 = (eps_r_pos_02 + 2*np.pi) % (2*np.pi)
    eps_r_pos_03 = (eps_r_pos_03 + 2*np.pi) % (2*np.pi)
    eps_r_pos_04 = (eps_r_pos_04 + 2*np.pi) % (2*np.pi)
    eps_r_neg_01 = (eps_r_neg_01 + 2*np.pi) % (2*np.pi)
    eps_r_neg_02 = (eps_r_neg_02 + 2*np.pi) % (2*np.pi)
    eps_r_neg_03 = (eps_r_neg_03 + 2*np.pi) % (2*np.pi)
    eps_r_neg_04 = (eps_r_neg_04 + 2*np.pi) % (2*np.pi)

    # Find closest index in B_theta_vec compared to rotor turn angles considering the periodicity of the angles between 0...2*pi
    idx_pos_01 = np.argmin(np.abs(B_theta_vec - eps_r_pos_01))
    idx_pos_02 = np.argmin(np.abs(B_theta_vec - eps_r_pos_02))
    idx_pos_03 = np.argmin(np.abs(B_theta_vec - eps_r_pos_03))
    idx_pos_04 = np.argmin(np.abs(B_theta_vec - eps_r_pos_04))
    idx_neg_01 = np.argmin(np.abs(B_theta_vec - eps_r_neg_01))
    idx_neg_02 = np.argmin(np.abs(B_theta_vec - eps_r_neg_02))
    idx_neg_03 = np.argmin(np.abs(B_theta_vec - eps_r_neg_03))
    idx_neg_04 = np.argmin(np.abs(B_theta_vec - eps_r_neg_04))

    # Calculate the Lorentz force acting on the rotor coils (independent of rotor current as it is a constant in all turns)
    F_r_pos_01 = B_hat * np.cos(B_theta_vec[idx_pos_01] - omega_s * t)
    F_r_pos_02 = B_hat * np.cos(B_theta_vec[idx_pos_02] - omega_s * t)
    F_r_pos_03 = B_hat * np.cos(B_theta_vec[idx_pos_03] - omega_s * t)
    F_r_pos_04 = B_hat * np.cos(B_theta_vec[idx_pos_04] - omega_s * t)
    F_r_neg_01 = B_hat * np.cos(B_theta_vec[idx_neg_01] - omega_s * t)
    F_r_neg_02 = B_hat * np.cos(B_theta_vec[idx_neg_02] - omega_s * t)
    F_r_neg_03 = B_hat * np.cos(B_theta_vec[idx_neg_03] - omega_s * t)
    F_r_neg_04 = B_hat * np.cos(B_theta_vec[idx_neg_04] - omega_s * t)   

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

    # plot the rotor DC current, i.e., a constant current of 1
    ax['ir'].plot(t_vec, np.ones_like(t_vec), color='black')

    # add y-axis labels ir/irmax LaTeX labels to rotor current subplots
    ax['ir'].set_ylabel(r'$i_{\mathrm{f}}(t)/i_{\mathrm{f,max}}$')

     # add vertical lines and markers to indicate the current time step for rotor currents
    ax['ir'].axvline(t, color='black', linestyle='--')
    ax['ir'].plot(t, 1, 'ko')
    
    # add x-axis label to the last row of subplots
    ax['isc'].set_xlabel(r'$t$ in s')
    ax['ir'].set_xlabel(r'$t$ in s')
   
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


    # plot circle for the first rotor turn position with pos current and add an inner gray circle to represent the pos current
    circle = plt.Circle((rotor_pos_01_rot[0], rotor_pos_01_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    circle = plt.Circle((rotor_pos_01_rot[0], rotor_pos_01_rot[1]), max_marker_size_circle, color='gray', fill=True)
    ax['motor'].add_artist(circle)

    # plot circle for the second rotor turn position with pos current and add an inner gray circle to represent the pos current
    circle = plt.Circle((rotor_pos_02_rot[0], rotor_pos_02_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    circle = plt.Circle((rotor_pos_02_rot[0], rotor_pos_02_rot[1]), max_marker_size_circle, color='gray', fill=True)
    ax['motor'].add_artist(circle)

    # plot circle for the third rotor turn position with pos current and add an inner gray circle to represent the pos current
    circle = plt.Circle((rotor_pos_03_rot[0], rotor_pos_03_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    circle = plt.Circle((rotor_pos_03_rot[0], rotor_pos_03_rot[1]), max_marker_size_circle, color='gray', fill=True)
    ax['motor'].add_artist(circle)

    # plot circle for the fourth rotor turn position with pos current and add an inner gray circle to represent the pos current
    circle = plt.Circle((rotor_pos_04_rot[0], rotor_pos_04_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    circle = plt.Circle((rotor_pos_04_rot[0], rotor_pos_04_rot[1]), max_marker_size_circle, color='gray', fill=True)
    ax['motor'].add_artist(circle)

    # plot circle for the first rotor turn position with neg current and add a inner gray x-marker to represent the neg current
    circle = plt.Circle((rotor_neg_01_rot[0], rotor_neg_01_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    ax['motor'].plot(rotor_neg_01_rot[0], rotor_neg_01_rot[1], 'x', markersize = max_marker_size_X, color='gray')

    # plot circle for the second rotor turn position with neg current and add a inner gray x-marker to represent the neg current
    circle = plt.Circle((rotor_neg_02_rot[0], rotor_neg_02_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    ax['motor'].plot(rotor_neg_02_rot[0], rotor_neg_02_rot[1], 'x', markersize = max_marker_size_X, color='gray')

    # plot circle for the third rotor turn position with neg current and add a inner gray x-marker to represent the neg current
    circle = plt.Circle((rotor_neg_03_rot[0], rotor_neg_03_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    ax['motor'].plot(rotor_neg_03_rot[0], rotor_neg_03_rot[1], 'x', markersize = max_marker_size_X, color='gray')

    # plot circle for the fourth rotor turn position with neg current and add a inner gray x-marker to represent the neg current
    circle = plt.Circle((rotor_neg_04_rot[0], rotor_neg_04_rot[1]), radius_coil, color='gray', fill=False)
    ax['motor'].add_artist(circle)
    ax['motor'].plot(rotor_neg_04_rot[0], rotor_neg_04_rot[1], 'x', markersize = max_marker_size_X, color='gray')

    # define left salient rotor edge
    rotor_polygon = plt.Polygon([rotor_salient_01_rot, rotor_salient_02_rot], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)

    # define right salient rotor edge
    rotor_polygon = plt.Polygon([rotor_salient_03_rot, rotor_salient_04_rot], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)

    # define upper salient pole arc
    rotor_upper_arc = patches.Arc(rotor_salient_05_rot, 1.75*radius_rotor_slot, 0.42, angle = eps * 180 / np.pi, theta1=0, theta2=180, color='black')
    ax['motor'].add_patch(rotor_upper_arc)

    # define lower salient pole arc
    rotor_lower_arc = patches.Arc(rotor_salient_06_rot, 1.75*radius_rotor_slot, 0.42, angle = eps * 180 / np.pi + 180, theta1=0, theta2=180, color='black')
    ax['motor'].add_patch(rotor_lower_arc)

    # connect upper salient pole arc with left salient rotor edge
    rotor_upper_arc_start = np.array([np.cos(eps), np.sin(eps)]) * 1.75/2*radius_rotor_slot + rotor_salient_05_rot
    rotor_polygon = plt.Polygon([rotor_salient_03_rot, rotor_upper_arc_start], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)

    # connect upper salient pole arc with right salient rotor edge
    rotor_lower_arc_start = np.array([np.cos(eps + np.pi), np.sin(eps + np.pi)]) * 1.75/2*radius_rotor_slot + rotor_salient_05_rot
    rotor_polygon = plt.Polygon([rotor_salient_01_rot, rotor_lower_arc_start], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)

    # connect lower salient pole arc with left salient rotor edge
    rotor_upper_arc_end = np.array([np.cos(eps), np.sin(eps)]) * 1.75/2*radius_rotor_slot + rotor_salient_06_rot
    rotor_polygon = plt.Polygon([rotor_salient_04_rot, rotor_upper_arc_end], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)

    # connect lower salient pole arc with right salient rotor edge
    rotor_lower_arc_end = np.array([np.cos(eps + np.pi), np.sin(eps + np.pi)]) * 1.75/2*radius_rotor_slot + rotor_salient_06_rot
    rotor_polygon = plt.Polygon([rotor_salient_02_rot, rotor_lower_arc_end], closed=True, fill=False, edgecolor='black')
    ax['motor'].add_artist(rotor_polygon)




    # make last tick of the isa subplot on x axis invisible
    ax['isa'].get_xticklabels()[-1].set_visible(False)

    #,ake first tick of the ir subplot on x axis invisible
    ax['ir'].get_xticklabels()[0].set_visible(False)




  
    # Plot the B field fundamental as a quiver plot with the starting points along the air gap and the direction of the arrows orthogonal to the air gap. The length of the arrows should be scaled by the B field strength - ensure that the number of arrows is not larger than 100
    n_arrows = 100
    idx = np.linspace(0, len(theta_vec)-1, n_arrows, dtype=int)
    for j in idx:
         B_handle = ax['motor'].quiver(np.cos(theta_vec[j]) * radius_air_gap - B[j]*np.cos(theta_vec[j])/6, np.sin(theta_vec[j]) * radius_air_gap - B[j]*np.sin(theta_vec[j])/6, B[j]*np.cos(theta_vec[j]), B[j]*np.sin(theta_vec[j]), color='gray', scale_units='xy', scale=3, width=0.005, label='B field')
    

    # Plot the Lorentz force acting on the rotor coils as a quiver plot with the starting points at the rotor coil positions and the direction of the arrows orthogonal to the rotor coil positions. The length of the arrows should be scaled by the Lorentz force acting on the rotor coils
    force_handle = ax['motor'].quiver(rotor_pos_01_rot[0], rotor_pos_01_rot[1], F_r_pos_01*np.cos(B_theta_vec[idx_pos_01] + np.pi/2), F_r_pos_01 * np.sin(B_theta_vec[idx_pos_01] + np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_pos_02_rot[0], rotor_pos_02_rot[1], F_r_pos_02*np.cos(B_theta_vec[idx_pos_02] + np.pi/2), F_r_pos_02 * np.sin(B_theta_vec[idx_pos_02] + np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_pos_03_rot[0], rotor_pos_03_rot[1], F_r_pos_03*np.cos(B_theta_vec[idx_pos_03] + np.pi/2), F_r_pos_03 * np.sin(B_theta_vec[idx_pos_03] + np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_pos_04_rot[0], rotor_pos_04_rot[1], F_r_pos_04*np.cos(B_theta_vec[idx_pos_04] + np.pi/2), F_r_pos_04 * np.sin(B_theta_vec[idx_pos_04] + np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_neg_01_rot[0], rotor_neg_01_rot[1], F_r_neg_01*np.cos(B_theta_vec[idx_neg_01] - np.pi/2), F_r_neg_01 * np.sin(B_theta_vec[idx_neg_01] - np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_neg_02_rot[0], rotor_neg_02_rot[1], F_r_neg_02*np.cos(B_theta_vec[idx_neg_02] - np.pi/2), F_r_neg_02 * np.sin(B_theta_vec[idx_neg_02] - np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_neg_03_rot[0], rotor_neg_03_rot[1], F_r_neg_03*np.cos(B_theta_vec[idx_neg_03] - np.pi/2), F_r_neg_03 * np.sin(B_theta_vec[idx_neg_03] - np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005)
    force_handle = ax['motor'].quiver(rotor_neg_04_rot[0], rotor_neg_04_rot[1], F_r_neg_04*np.cos(B_theta_vec[idx_neg_04] - np.pi/2), F_r_neg_04 * np.sin(B_theta_vec[idx_neg_04] - np.pi/2), color='#7401d8ff', scale_units='xy', scale=3, width=0.005, label='Lorentz force')

    

    # set motor subplot limits to -1.5 to 1.5 in both x and y directions
    ax['motor'].set_xlim(-1.5, 1.5)
    ax['motor'].set_ylim(-1.5, 1.5)

    # set ir y axis identical to isa y axis
    ax['ir'].set_ylim(ax['isa'].get_ylim())
    
    # set motor subplot aspect ratio to be equal
    ax['motor'].set_aspect('equal')

    #set the legend entries vertically stacked over each other
    ax['motor'].legend((B_handle, force_handle), ('B field (stator normal component, fundamental)', 'Lorentz force'), loc='lower center', ncol=1, fancybox=True, bbox_to_anchor=(0.5, -0.05))



#update_plot(30)
#plt.show()

current_directory = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_directory, 'SM_load_angle_0_animation.gif')
ani = animation.FuncAnimation(fig, update_plot, frames=n_frames, repeat=True)
ani.save(save_path, writer='imagemagick', fps=25)
plt.show()



