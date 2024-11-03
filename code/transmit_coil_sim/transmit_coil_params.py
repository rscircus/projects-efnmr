import numpy as np
import matplotlib.pyplot as plt

Brng = np.exp(np.linspace(np.log(1e-6), np.log(1e-3), 101))
Brng_coarse = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3]

Nrng = np.exp(np.linspace(np.log(10), np.log(10000), 101))
Nrng_coarse = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]


# t/r coil from Michal 2010
R0 = 0.1 # resistance per winding
r = 0.050
l = 0.100
A = np.pi*r**2
mu0 = 4e-7*np.pi
L0 = mu0*A/l
b0 = mu0/l

w0 = 2*np.pi*2.1e3
Z0 = w0*L0 # reactance per winding squared

plt.figure(figsize=(6, 6))

for B in Brng_coarse:
    I = B/(b0*Nrng)
    V = B*np.sqrt(R0**2+Z0**2*Nrng**2)/b0
    plt.loglog(V, I, "r-", lw=2 if B!=5e-5 else 4)
    plt.text(V[-1], I[-1], f"{B/1e-6:.2f} uT",
        ha="left",
        va="top",
        color="red")

for N in Nrng_coarse:
    I = Brng/(b0*N)
    V = Brng*np.sqrt(R0**2+Z0**2*N**2)/b0
    plt.loglog(V, I, "b-", lw=2)
    plt.text(V[-1], I[-1], f"{N} windings",
        ha="left",
        va="bottom",
        color="blue")

plt.xlim((5e-3, 4e4))
plt.xlabel("Voltage [V]")
plt.ylabel("Current [A]")
plt.grid()
plt.tight_layout()
plt.show()
