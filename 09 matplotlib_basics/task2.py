import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


# Данные и функция
X = np.arange(0.1, 10, 0.25)
Y = np.arange(0.1, 10, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.log(X * Y)

# 1. Рисуем 3D-поверхность
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

# 2. Рисуем контурную диаграмму
a = np.array([X, Y, Z])
fig = plt.figure()
plt.contour(a[0], a[1], a[2], cmap=cm.coolwarm)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

# 3.1 Рисуем изображение
fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation='bilinear', cmap=cm.coolwarm,
               origin='lower', extent=[-3, 3, -3, 3],
               vmax=abs(Z).max(), vmin=-abs(Z).max())
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

# 3.2 Сохраняем изображение
fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation='bilinear', cmap=cm.coolwarm,
               origin='lower', extent=[-3, 3, -3, 3],
               vmax=abs(Z).max(), vmin=-abs(Z).max())
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('image.png')

