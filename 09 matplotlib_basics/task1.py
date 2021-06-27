import numpy as np
import matplotlib.pyplot as plt

ax = plt.figure().add_subplot(projection='3d')

t = np.linspace(-10, 10, 100)
x = t
y = np.cosh(t)
z = t
ax.plot(x, y, z, label='x=t, y=cosh(t), z=t')
ax.legend()

plt.show()


