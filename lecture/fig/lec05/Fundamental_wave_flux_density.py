import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

B_hat = 1
p = 1
omega = 50 * 2 * np.pi
theta_vec = np.linspace(0, 2*np.pi, 100)
t = 0

B_a = B_hat / 2 * (np.sin(theta_vec * p - omega * t) + np.sin(theta_vec *p + omega * t))
B_b = B_hat / 2 * (np.sin(theta_vec * p - omega * t) + np.sin(theta_vec *p + omega * t - 4*np.pi/3))
B_c = B_hat / 2 * (np.sin(theta_vec * p - omega * t) + np.sin(theta_vec *p + omega * t - 8*np.pi/3))

B = B_a + B_b + B_c


#Plot the flux densities in seperate subplots stacked vertically
fig, ax = plt.subplots(4, 1, figsize=(6, 8))
ax[0].plot(theta_vec, B_a, 'r')
ax[1].plot(theta_vec, B_b, 'b')
ax[2].plot(theta_vec, B_c, 'g')
ax[3].plot(theta_vec, B, 'k')

#plt.tight_layout()

#add a single x-axis label to the bottom plot
ax[3].set_xlabel(r'$\vartheta$')

#modify x-axis to show tick labels in fractions of pi for only the last subplot while the others are hidden
for i in range(3):
    ax[i].set_xticklabels([])
    ax[i].set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax[3].set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax[3].set_xticklabels(['$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])





#add background grids to all subplots
for i in range(4):
    ax[i].grid(True)

#add y-labels to the subplots in the style B_i/\hat{B}_\delta
for i in range(3):
    ax[i].set_ylabel(r'$B^{(1)}_\mathrm{' + chr(ord('a') + i) + r'}(\vartheta)/\hat{B}_\delta$')
ax[3].set_ylabel(r'$B^{(1)}_\Sigma(\vartheta)/\hat{B}_\delta$')

#set the x-axis limits to [0, 2*pi]
for i in range(4):
    ax[i].set_xlim([0, 2*np.pi])


#set the y-axis limits to [-3/2, 3/2]
for i in range(4):
    ax[i].set_ylim([-3/2, 3/2])






plt.show()




