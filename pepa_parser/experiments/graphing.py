#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from pylab import plot, ylabel, xlabel, show, savefig

def plot_2d(xs, ys, lw=1, xlab="X", ylab="Y", action="show", name="NONAME-2d"):
    plot(xs, ys, linewidth=lw)
    xlabel("{}".format(xlab))
    ylabel("{} throughoutput".format(ylab))
    if action == "show":
        show()
    else:
        savefig("{}.png".format(name))

def plot_3d(xs, ys, zs, xlab="X", ylab="Y", action="show", name="NONAME-3d"):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, zs, rstride=1, cstride=1, cmap=cm.jet,
                    linewidth=0, antialiased=False)
    plt.show()




