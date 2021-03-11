import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import correlate


data = np.load('30x30_500ticksStrats(1).npy')
AR = data[0]
AP = data[1]
AS = data[2]
t = np.arange(0, 501)

fig1, ax1 = plt.subplots()
ax1.plot(t, AR, label='Always Rock')
ax1.plot(t, AP, label='Always Paper')
ax1.plot(t, AS, label='Always Scissors')
ax1.set(xlabel='Clock tick (t)', ylabel='Population')
plt.legend(loc='upper right')
plt.show()

cutoff = 301

n = len(t[cutoff:])
freqs = fftfreq(n)
mask = freqs > 0
ARfft = 2*np.abs(fft(AR[cutoff:]) / n)
APfft = 2*np.abs(fft(AP[cutoff:]) / n)
ASfft = 2*np.abs(fft(AS[cutoff:]) / n)

fig2, ax2 = plt.subplots()
ax2.plot(freqs[mask], ARfft[mask], label='Always Rock - FFT')
ax2.plot(freqs[mask], APfft[mask], label='Always Paper - FFT')
ax2.plot(freqs[mask], ASfft[mask], label='Always Scissors - FFT')
ax2.set(xlabel='Frequency', ylabel='Amplitude')
ax2.grid()
plt.legend(loc='upper right')
plt.show()


n = len(t[cutoff:])
AR = AR[cutoff:]
AR = AR - np.mean(AR)
AR = AR / np.std(AR)

AP = AP[cutoff:]
AP = AP - np.mean(AP)
AP = AP / np.std(AP)

AS = AS[cutoff:]
AS = AS - np.mean(AS)
AS = AS / np.std(AS)


RP_corr = correlate(AR, AP)
RS_corr = correlate(AR, AS)
PS_corr = correlate(AP, AS)


dt = np.arange(1-n, n)
RPtime_shift = dt[RP_corr.argmax()]
RStime_shift = dt[RS_corr.argmax()]
PStime_shift = dt[PS_corr.argmax()]

#%%

x = np.arange(0, 2*np.pi, np.pi/64)
S1 = np.sin(x)
S2 = np.sin(x + (np.pi/4))

plt.plot(x, S1)
plt.plot(x, S2)
plt.show()

n = len(x)
corr = np.correlate(S1, S2, 'full')

