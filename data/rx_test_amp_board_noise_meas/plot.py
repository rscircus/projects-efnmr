"""
Spectrum measured with the RTB2004 at RBW = 10Hz, ac coupling (2 Hz cutoff)
Frequency in Hz, power in dBV
"""

import matplotlib.pyplot as plt
import numpy as np

def load_psd(filename, RBW=10.0):
    data = []
    with open(filename, "r") as f:
        for line in list(f)[1:]:
            data.append([float(s) for s in line.split(",")])
    data = np.array(data)
    data[:, 1] = np.sqrt(10.0**(data[:, 1]/10)/RBW) # convert to V/sqrt(Hz)
    return data

data_amp = load_psd("AMP.CSV")
data_bg = load_psd("BG.CSV")

plt.semilogy(data_amp[:, 0], data_amp[:, 1], label="amplifier output")
plt.semilogy(data_amp[:, 0], data_amp[:, 1]-data_bg[:, 1], label="amplifier output (background subtracted)")
plt.semilogy(data_bg[:, 0], data_bg[:, 1], label="background")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [$\\mathrm{V}/\\sqrt{\\mathrm{Hz}}$]")
plt.ylim((1e-6, 4e-4))
plt.show()
