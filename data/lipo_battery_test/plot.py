import numpy as np
import matplotlib.pyplot as plt
import scipy

data = []

with open("241102_discharge_15R.txt", "r") as f:
    for line in f:
        if line.startswith("#"):
            continue

        time_str, v_str = line.split(" ")
        h_str, m_str = time_str.split(":")

        time_min = float(h_str)*60.0 + float(m_str)
        v = float(v_str)
        data.append([time_min, v])

data = np.array(data)
data[:, 0] -= data[0, 0]

data_interp = scipy.interpolate.interp1d(data[:, 0], data[:, 1])
time_fine = np.linspace(data[0, 0], data[-1, 0], 401)
dt = time_fine[1]-time_fine[0]
v_fine = np.array([data_interp(t) for t in time_fine])
R = 15.4
c_fine = np.cumsum(v_fine/R)*60.0*dt

plt.subplot(2, 1, 1)
plt.plot(data[:, 0], data[:, 1], "o")
plt.plot(time_fine, v_fine, "-")
plt.grid()
plt.xlabel("Time [min]")
plt.ylabel("Voltage [V]")

plt.subplot(2, 1, 2)
plt.plot(c_fine/3.6, v_fine, "-")
plt.grid()
plt.xlabel("Charge [mAh]")
plt.ylabel("Voltage [V]")


plt.show()
