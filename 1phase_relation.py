import numpy as np
import matplotlib.pyplot as plt

file1 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(1)_30x30_1000ticksStrats.npy'
data1 = np.load(file1)
AR1 = data1[0]
AP1 = data1[1]
AS1 = data1[2]
t1 = np.arange(0, len(AR1))

file3 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(3)_30x30_1000ticksStrats.npy'
data3= np.load(file3)
AR3 = data3[0]
AP3 = data3[1]
AS3 = data3[2]
t3 = np.arange(0, len(AR3))

file5 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(5)_30x30_1000ticksStrats.npy'
data5 = np.load(file5)
AR5 = data5[0]
AP5 = data5[1]
AS5 = data5[2]
t5 = np.arange(0, len(AR5))

file8 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(8)_30x30_1000ticksStrats.npy'
data8 = np.load(file8)
AR8 = data8[0]
AP8 = data8[1]
AS8 = data8[2]
t8 = np.arange(0, len(AR8))

file19 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(19)_30x30_1000ticksStrats.npy'
data19 = np.load(file19)
AR19 = data19[0]
AP19 = data19[1]
AS19 = data19[2]
t19 = np.arange(0, len(AR19))

file20 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(20)_30x30_1000ticksStrats.npy'
data20 = np.load(file20)
AR20 = data20[0]
AP20 = data20[1]
AS20 = data20[2]
t20 = np.arange(0, len(AR20))

file22 = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project' \
            r'\GCM\30x30_ROTATION\(22)_30x30_1000ticksStrats.npy'
data22 = np.load(file22)
AR22 = data22[0]
AP22 = data22[1]
AS22 = data22[2]
t22 = np.arange(0, len(AR22))

#%%

upto = 15
std_data1 = []
std_data3 = []
std_data5 = []
std_data8 = []
std_data19 = []
std_data20 = []
std_data22 = []
for i in range(upto + 1):
    std_data1.append(AR1[i])
    std_data1.append(AP1[i])
    std_data1.append(AS1[i])
    
    std_data3.append(AR3[i])
    std_data3.append(AP3[i])
    std_data3.append(AS3[i])
    
    std_data5.append(AR5[i])
    std_data5.append(AP5[i])
    std_data5.append(AS5[i])
    
    std_data8.append(AR8[i])
    std_data8.append(AP8[i])
    std_data8.append(AS8[i])
    
    std_data19.append(AR19[i])
    std_data19.append(AP19[i])
    std_data19.append(AS19[i])

    std_data20.append(AR20[i])
    std_data20.append(AP20[i])
    std_data20.append(AS20[i])
    
    std_data22.append(AR22[i])
    std_data22.append(AP22[i])
    std_data22.append(AS22[i])
    
std = [np.std(std_data1), np.std(std_data3), np.std(std_data5), \
       np.std(std_data8), np.std(std_data19), np.std(std_data20), \
           np.std(std_data22)]
time = [97, 183, 130, 226, 131, 107, 139]

zipped_lists = zip(std, time)
sorted_pairs = sorted(zipped_lists)
tuples = zip(*sorted_pairs)
std, time = [list(tuple) for tuple in tuples]

std = np.array(std)
time = np.array(time)

coeffs = np.polyfit(std, time, 1)
func = np.poly1d(coeffs)
#x = np.linspace(20, 80, 1000)

fig1, ax1 = plt.subplots()
ax1.errorbar(std, time, xerr=None, yerr=5, capsize=3, fmt='bo', zorder=2, \
             label='Raw Data')
ax1.plot(std, func(std), 'r--', zorder=1, \
         label='y = {}x + {}'.format(coeffs[0], coeffs[1]))
ax1.set(xlabel=r'Standard deviation, $\sigma$', \
        ylabel='Time to reach steady state')
handles, labels = ax1.get_legend_handles_labels()
handles.reverse()
labels.reverse()
ax1.legend(handles, labels, loc='upper left')
plt.show()
    

