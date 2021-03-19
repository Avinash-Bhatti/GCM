import numpy as np
import matplotlib.pyplot as plt

file = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(19)_30x30_1000ticksStrats.npy'
data = np.load(file)

AR = data[0]
AP = data[1]
AS = data[2]
t = np.arange(0, len(AR))

fig, ax = plt.subplots()
ax.plot(t, AR, label='Always Rock')
ax.plot(t, AP, label='Always Paper')
ax.plot(t, AS, label='Always Scissors')
ax.axvline(x=250, color='k')
ax.axvline(x=500, color='k')
ax.axvline(x=750, color='k')
ax.set(xlabel='Clock tick', ylabel='Population', \
       xticks=np.arange(0, 1050, 50))
plt.legend(loc='upper right')
plt.show()