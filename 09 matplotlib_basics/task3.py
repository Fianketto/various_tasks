import numpy as np
import matplotlib.pyplot as plt


# Функции
x = np.linspace(-np.pi, np.pi, 500)
f = np.sin(x ** 2)
g = np.cos(x ** 2)


# 1. Разные окна
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)

ax.grid(which='both')
ax.plot(x, f, 'r', label='f(x)=sin(x^2)', linewidth=6)

plt.xlabel("x")
plt.ylabel("f(x)")
ax.legend()

fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)

ax.grid(which='both')
ax.plot(x, g, 'b', label='g(x)=cos(x^2)', linewidth=6)

plt.xlabel("x")
plt.ylabel("g(x)")
ax.legend()

plt.show()


# 2. Одно окно, одни оси
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.grid(which='both')

line1, = ax.plot(x, f, 'r', label='f(x)=sin(x^2)')
line2, = ax.plot(x, g, 'b', label='g(x)=cos(x^2)')
line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break
line2.set_dashes([2, 2])

plt.xlabel("x")
plt.ylabel("f(x), g(x)")
ax.legend()

plt.show()


# 3. Одно окно, разные оси
fig = plt.figure()

ax_1 = fig.add_subplot(3, 1, 1)
ax_2 = fig.add_subplot(3, 1, 3)

ax_1.set(title='f(x)=sin(x)')
ax_2.set(title='g(x)=cos(x)')
ax_1.grid(which='both')
ax_2.grid(which='both')

line1 = ax_1.plot(x, f, 'g', label='f(x)=sin(x^2)')
line2 = ax_2.plot(x, g, 'y', label='f(x)=cos(x^2)')

plt.show()


