import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

t = np.arange(0.0, 2.0, 0.01)

fig, ax = plt.subplots()
lines = []
for i in range(1, 5):
    s = np.sin(i*np.pi*t)
    l, = ax.plot(t, s, lw=2, label="%s Hz"%i)
    lines.append(l)

plt.subplots_adjust(left=0.2)


# Make checkbuttons with all plotted lines with correct visibility
rax = plt.axes([0.05, 0.5, 0.1, 0.2])  # 4-tuple of floats rect = [left, bottom, width, height]
labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)


def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

check.on_clicked(func)

plt.show()