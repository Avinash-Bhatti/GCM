import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.optimize import curve_fit

file = r'C:\Users\Avinash\Documents\Uni\Year3\Term2\Project\GCM\30x30' \
        r'\(1)_30x30_500ticksStrats.npy'
data = np.load(file)

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

cutoff = 200
t_ = t[cutoff:]
#t_ -= cutoff
n = len(t_)
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


AR_ = AR[cutoff:]
AP_ = AP[cutoff:]
AS_ = AS[cutoff:]


##############################################################################

'''
https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-
data-with-pylab-and-numpy
'''


def fit_sin(tt, yy):
    
    '''
    Fit sin to the input time sequence, and return fitting parameters "amp",
    "omega", "phase", "offset", "freq", "period" and "fitfunc"
    '''
    
    tt = np.array(tt)
    yy = np.array(yy)
    # assume uniform spacing
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))
    Fyy = abs(np.fft.fft(yy))
    # excluding the zero frequency "peak", which is related to offset
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, \
            "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), \
                "rawres": (guess,popt,pcov)}

##############################################################################

tt_ = np.linspace(min(t_), max(t_), 100000)
n_ = len(tt_)

res_R = fit_sin(t_, AR_)
res_P = fit_sin(t_, AP_)
res_S = fit_sin(t_, AS_)

fig3, ax3 = plt.subplots()
ax3.plot(tt_, res_R['fitfunc'](tt_), label='AR fit')
ax3.plot(tt_, res_P['fitfunc'](tt_), label='AP fit')
ax3.plot(tt_, res_S['fitfunc'](tt_), label='AS fit')
ax3.set(xlabel='Clock tick (t)', ylabel='Population')
plt.legend(loc='upper right')
plt.show()

'''

corr_RR = correlate(res_R['fitfunc'](tt_), res_R['fitfunc'](tt_))
corr_PP = correlate(res_P['fitfunc'](tt_), res_P['fitfunc'](tt_))

RR = np.argmax(corr_RR)
PP = np.argmax(corr_PP)

corr_RP = correlate(res_R['fitfunc'](tt_), res_P['fitfunc'](tt_))
corr_RS = correlate(res_R['fitfunc'](tt_), res_S['fitfunc'](tt_))
corr_PS = correlate(res_P['fitfunc'](tt_), res_S['fitfunc'](tt_))

RP = np.argmax(corr_RP)
RS = np.argmax(corr_RS)
PS = np.argmax(corr_PS)

phase_RP = ((tt_[-1])*(RR-RP)) / n_
phase_RS = ((tt_[-1])*(RR-RS)) / n_
phase_PS = ((tt_[-1])*(PP-PS)) / n_

'''


#%%

end = 10*np.pi
x = np.arange(0, end, np.pi/64)
n = len(x)

S1 = np.sin(x)
S2 = np.sin(x + (np.pi/1))

plt.plot(x, S1)
plt.plot(x, S2)
plt.show()

corr1 = correlate(S1, S1)
corr2 = correlate(S1, S2)

a1 = np.argmax(corr1)
a2 = np.argmax(corr2)

phase = ((end)*(a1 - a2)) / n
print(phase / np.pi)



