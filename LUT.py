import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d

ax = plt.axes(projection="3d")

x_data = np.arange(0,50,0.1)
y_data = np.arange(0,50,0.1)
y_data = np.sin(y_data)
z_data = x_data*y_data

#ax.scatter(x_data,y_data,z_data)
ax.plot(x_data,y_data,z_data)
plt.show()