# February 12, 2018

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
fig = plt.figure(facecolor='#07000d')
# 272822 monokai
# 07000d purple black
fig.canvas.set_window_title('Time vs Fitness')
ax1 = fig.add_subplot(1, 1, 1, facecolor='#07000d')

# clears the file every time program is started
pulldata = open('FitData.txt', 'w')
pulldata.close()


def animate(i):
    pulldata = open('FitData.txt', 'r').read()
    dataArray = pulldata.split('\n')
    xar = []
    yar = []
    for line in dataArray:
        if len(line) > 1:
            x, y = line.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    plt.xlabel('Time(per tick)', color='#ABAA98')
    plt.ylabel('Fitness', color='#ABAA98')
    ax1.tick_params(axis='y', colors='#ABAA98')
    ax1.tick_params(axis='x', colors='#ABAA98')
    ax1.plot(xar, yar, color='#66D9EF')
    ax1.spines['bottom'].set_color('#5998ff')
    ax1.spines['left'].set_color('#5998ff')
    ax1.spines['right'].set_color('#5998ff')
    ax1.spines['top'].set_color('#5998ff')
    ax1.grid(True, color='#ABAA98', alpha=0.2, linewidth='0.5')


ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()
