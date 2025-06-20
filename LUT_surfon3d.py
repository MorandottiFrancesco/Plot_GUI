import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d

ax = plt.axes(projection="3d")

x_data = np.arange(-1,1,0.1)
y_data = np.arange(-5,5,0.1)

X, Y = np.meshgrid(x_data, y_data)

Z = np.sin(X) * np.cos(Y)


#ax.scatter(x_data,y_data,z_data)
ax.plot_surface(X, Y, Z, cmap='plasma')

ax.set_title("3D Line Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")


plt.show()