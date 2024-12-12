import numpy as np
import matplotlib.pyplot as plt
from opamp_circuit import Circuit, Resistor, Capacitor, IdealOpAmp, \
    IdealVoltageSource, IdealCurrentSource

if __name__ == "__main__":
    R1 = 330.0
    R2 = 330.0e3
    R3 = 15.0e3
    R4 = 370.0
    C1 = 10.0e-9
    C2 = 10.0e-9
    R5 = 150.0e3
    R6 = 2.0e3
    R7 = 1.5e3
    R8 = 15.0e3
    circuit = Circuit()
    circuit.add(Resistor(R1, ["oa1_in_inv", "gnd"], name="R1"))
    circuit.add(Resistor(R2, ["oa1_in_inv", "oa1_out"], name="R2"))
    circuit.add(IdealOpAmp(["oa1_in_noninv", "oa1_in_inv", "oa1_out"], name="OA1"))
    circuit.add(IdealVoltageSource("Vin", ["oa1_in_noninv", "gnd"]))
    circuit.add(Resistor(R3, ["oa1_out", "int1"], name="R3"))
    circuit.add(Resistor(R4, ["int1", "gnd"], name="R4"))
    circuit.add(Capacitor(C1, ["int1", "oa2_in_inv"], name="C1"))
    circuit.add(Capacitor(C2, ["int1", "oa2_out"], name="C2"))
    circuit.add(Resistor(R5, ["oa2_in_inv", "oa2_out"], name="R5"))
    circuit.add(IdealOpAmp(["gnd", "oa2_in_inv", "oa2_out"], name="OA2"))
    circuit.add(Resistor(R6, ["gnd", "oa2_out"], name="R6"))
    circuit.add(Resistor(R7, ["oa2_out", "oa3_in_inv"], name="R7"))
    circuit.add(Resistor(R8, ["oa3_in_inv", "oa3_out"], name="R8"))
    circuit.add(IdealOpAmp(["gnd", "oa3_in_inv", "oa3_out"], name="OA3"))
    circuit.add_noise_sources()

    def gain_th(w):
        Gbp = -1j*w*C1*R5/R3/(1/R3+1/R4+1j*w*C1+1j*w*C2*(1+1j*w*C1*R5))
        return (1+R2/R1)*Gbp*(-R8/R7)

    frange = np.exp(np.linspace(np.log(10.0), np.log(10000.0), 1501))
    gains = []
    gains_th = []
    for f in frange:
        sol = circuit.solve(2*np.pi*f)
        gain = sol["Vin"]["oa3_out"]
        gains.append(gain)
        gains_th.append(gain_th(2*np.pi*f))
    gains = np.array(gains)
    gains_th = np.array(gains_th)

    assert max(abs(gains_th-gains)) < 1e-6, "gain calculation failed"

    plt.loglog(frange, abs(gains))
    plt.loglog(frange, abs(gains_th), "--")
    plt.grid()
    plt.show()


    frange = np.linspace(0, 5000, 1001)
    noiseAmpV = []
    noiseAmpI = []
    noiseRes = []
    for f in frange:
        sol = circuit.solve(2*np.pi*f)
        noiseAmpV.append(abs(sol["Vnoise_OA1"]["oa3_out"])**2 + abs(sol["Vnoise_OA2"]["oa3_out"])**2 + abs(sol["Vnoise_OA3"]["oa3_out"])**2)
        noiseAmpI.append(
            abs(sol["Inoise1_OA1"]["oa3_out"])**2 + abs(sol["Inoise1_OA2"]["oa3_out"])**2 + abs(sol["Inoise1_OA3"]["oa3_out"])**2 +
            abs(sol["Inoise2_OA1"]["oa3_out"])**2 + abs(sol["Inoise2_OA2"]["oa3_out"])**2 + abs(sol["Inoise2_OA3"]["oa3_out"])**2)
        noiseRes.append(sum([c.R*abs(sol[f"Vnoise_{c.name}"]["oa3_out"])**2 for c in circuit.components if isinstance(c, Resistor)]))
    noiseAmpV = np.array(noiseAmpV)
    noiseAmpI = np.array(noiseAmpI)
    noiseRes = np.array(noiseRes)

    plt.semilogy(frange, np.sqrt(noiseAmpV)*2.2e-9)
    plt.semilogy(frange, np.sqrt(noiseAmpI)*5.0e-13)
    plt.semilogy(frange, np.sqrt(4*1.38e-23*300*noiseRes))
    plt.grid()
    plt.xlim((0, 5000))
    plt.ylim((1e-6, 1e-3))
    plt.show()
