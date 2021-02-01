# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 21:49:24 2021

@author: Alex
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Fixing random state for reproducibility
np.random.seed(19680801)


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)




fig2 = plt.figure()

x = np.arange(0, 10)
y = np.arange(0, 10).reshape(-1, 1)
base = np.hypot(x, y)
ims = []
for add in np.arange(35):
    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=200, repeat_delay=3000,
                                   blit=True)
im_ani.save('im.mp4', writer=writer)