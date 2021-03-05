import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import correlate

data = np.load('30x30_500ticksStrats.npy')
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

n = len(t[201:])
freqs = fftfreq(n)
mask = freqs > 0
ARfft = 2*np.abs(fft(AR[201:]) / n)
APfft = 2*np.abs(fft(AP[201:]) / n)
ASfft = 2*np.abs(fft(AS[201:]) / n)

fig2, ax2 = plt.subplots()
ax2.plot(freqs[mask], ARfft[mask], label='Always Rock - FFT')
ax2.plot(freqs[mask], APfft[mask], label='Always Paper - FFT')
ax2.plot(freqs[mask], ASfft[mask], label='Always Scissors - FFT')
ax2.set(xlabel='Frequency', ylabel='Amplitude')
ax2.grid()
plt.legend(loc='upper right')
plt.show()


#%%

n = len(t[201:])
AR = AR[201:]
AR = AR - np.mean(AR)
AR = AR / np.std(AR)

AP = AP[201:]
AP = AP - np.mean(AP)
AP = AP / np.std(AP)

AS = AS[201:]
AS = AS - np.mean(AS)
AS = AS / np.std(AS)


RP_corr = correlate(AR, AP)
RS_corr = correlate(AR, AS)
PS_corr = correlate(AP, AS)


dt = np.arange(1-n, n)
RPtime_shift = dt[RP_corr.argmax()]
RStime_shift = dt[RS_corr.argmax()]
PStime_shift = dt[PS_corr.argmax()]



