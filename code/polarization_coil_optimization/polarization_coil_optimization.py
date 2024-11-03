import numpy as np
import matplotlib.pyplot as plt

wires = [
    {"pn": "distrelec:304-05-595", "cross-section": 0.4e-6, "cost_chf_per_m": 33.58/120},
    {"pn": "distrelec:304-05-594", "cross-section": 0.26e-6, "cost_chf_per_m": 35.13/200},
    {"pn": "distrelec:304-05-593", "cross-section": 0.13e-6, "cost_chf_per_m": 37.15/400},
    {"pn": "distrelec:304-04-210", "cross-section": 0.08e-6, "cost_chf_per_m": 38.39/700},
    {"pn": "distrelec:155-50-339", "cross-section": 0.12e-6, "cost_chf_per_m": 18.27/138},
    {"pn": "distrelec:155-18-006", "cross-section": 0.79e-6, "cost_chf_per_m": 79.45/140},
    {"pn": "distrelec:155-17-834", "cross-section": 0.50e-6, "cost_chf_per_kg": 10.22/0.1},
    ]

coil_radius = 3e-2
coil_length = 8e-2
mu0 = 4e-7*np.pi
B = 0.1

coil_perimeter = 2*np.pi*coil_radius

I_N = B*coil_length/mu0

for wire in wires:
    if "cost_chf_per_kg" in wire:
        wire["cost_chf_per_m"] = wire["cost_chf_per_kg"]*8935.0*wire["cross-section"]
    else:
        wire["cost_chf_per_kg"] = wire["cost_chf_per_m"]/(8935.0*wire["cross-section"])

    wire["resistance_ohm_per_m"] = 16.78e-9/wire["cross-section"]

I_range = 5.0 * np.exp(np.linspace(-2.0, 2.0, 21))
N_range = I_N / I_range

plt.subplot(2, 2, 1)
for wire in wires:
    V_range = coil_perimeter * N_range * wire["resistance_ohm_per_m"] * I_range
    cost_range = coil_perimeter * N_range * wire["cost_chf_per_m"]
    label = wire['pn'].split(':')[1] + ", " + f"{wire['cross-section']/1e-6:.2f}" + "$\\mathrm{mm}^2$"

    plt.loglog(V_range * I_range, cost_range, "o", label=label)

plt.xlabel("Power [W]")
plt.ylabel("Cost [CHF]")
plt.legend()
plt.grid()

plt.subplot(2, 2, 2)
for wire in wires:
    V_range = coil_perimeter * N_range * wire["resistance_ohm_per_m"] * I_range
    cost_range = coil_perimeter * N_range * wire["cost_chf_per_m"]
    label = wire['pn'].split(':')[1] + ", " + f"{wire['cross-section']/1e-6:.2f}" + "$\\mathrm{mm}^2$"

    plt.loglog(V_range, I_range, "o", label=label)

plt.xlabel("Voltage [V]")
plt.ylabel("Current [A]")
plt.legend()
plt.grid()

plt.subplot(2, 2, 3)
for wire in wires:
    V_range = coil_perimeter * N_range * wire["resistance_ohm_per_m"] * I_range
    cost_range = coil_perimeter * N_range * wire["cost_chf_per_m"]
    label = wire['pn'].split(':')[1] + ", " + f"{wire['cross-section']/1e-6:.2f}" + "$\\mathrm{mm}^2$"

    L_range = B * np.pi * coil_radius**2 * N_range / I_range

    plt.loglog(V_range * I_range, L_range, "o", label=label)

plt.xlabel("Power [W]")
plt.ylabel("Inductance [H]")
plt.legend()
plt.grid()

plt.subplot(2, 2, 4)
for wire in wires:
    R_range = coil_perimeter * N_range * wire["resistance_ohm_per_m"]
    V_range = R_range * I_range
    cost_range = coil_perimeter * N_range * wire["cost_chf_per_m"]
    label = wire['pn'].split(':')[1] + ", " + f"{wire['cross-section']/1e-6:.2f}" + "$\\mathrm{mm}^2$"

    L_range = B * np.pi * coil_radius**2 * N_range / I_range

    plt.loglog(V_range * I_range, L_range/R_range, "o", label=label)

plt.xlabel("Power [W]")
plt.ylabel("Decay time [s]")
plt.legend()
plt.grid()

plt.show()
