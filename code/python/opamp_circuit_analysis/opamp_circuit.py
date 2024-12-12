import numpy as np
import matplotlib.pyplot as plt

def merge_node_groups(node_groups, key1, key2):
    idx1 = [i for i, g in enumerate(node_groups) if key1 in g][0]
    idx2 = [i for i, g in enumerate(node_groups) if key2 in g][0]
    if idx1 == idx2:
        return
    else:
        node_groups[idx1] += node_groups[idx2]
        del node_groups[idx2]

class Component:
    def __init__(self, Y, nodes, name=None):
        self.Y = Y
        self.nodes = nodes
        self._name = name

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return f"c{abs(hash(self))}"

class Resistor(Component):
    def __init__(self, R, nodes, **kwargs):
        self.R = R
        Component.__init__(self, lambda w: 1/R, nodes, **kwargs)

class Capacitor(Component):
    def __init__(self, C, nodes, **kwargs):
        self.C = C
        Component.__init__(self, lambda w: 1j*w*C, nodes, **kwargs)

class IdealOpAmp(Component):
    def __init__(self, nodes, **kwargs):
        Component.__init__(self, None, nodes, **kwargs)

class IdealVoltageSource(Component):
    def __init__(self, name, nodes, **kwargs):
        Component.__init__(self, None, nodes, name=name, **kwargs)

class IdealCurrentSource(Component):
    def __init__(self, name, nodes, **kwargs):
        Component.__init__(self, None, nodes, name=name, **kwargs)

class Circuit:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def component(self, name):
        return [c for c in self.components if c.name==name][0]

    def nodes(self, exclude_ground=False):
        nodes_lst = []
        for component in self.components:
            nodes_lst += component.nodes
        nodes_lst = sorted(list(set(nodes_lst)))
        if exclude_ground:
            nodes_lst = [n for n in nodes_lst if n != "gnd"]
        return nodes_lst

    def add_noise_sources(self):
        new_components = []
        for component in self.components:
            if isinstance(component, Resistor):
                node1, node2 = component.nodes
                nodeI = f"_internal_{component.name}"
                component.nodes[1] = nodeI
                new_components.append(
                    IdealVoltageSource(f"Vnoise_{component.name}", [nodeI, node2])
                    )
            if isinstance(component, IdealOpAmp):
                nodeNonInv, nodeInv, nodeOut = component.nodes
                nodeI = f"_internal_{component.name}"
                component.nodes[0] = nodeI
                new_components.append(
                    IdealVoltageSource(f"Vnoise_{component.name}", [nodeNonInv, nodeI])
                    )
                new_components.append(
                    IdealCurrentSource(f"Inoise1_{component.name}", [nodeNonInv, "gnd"])
                    )
                new_components.append(
                    IdealCurrentSource(f"Inoise2_{component.name}", [nodeInv, "gnd"])
                    )
        self.components += new_components

    def solve(self, w):
        nodes = self.nodes()
        dim = len(nodes)
        Y = np.zeros((dim, dim), dtype=complex)
        node_groups = [[node] for node in nodes]
        voltage_constraints = []
        voltage_constraints_keys = []
        for component in self.components:
            if component.Y is not None:
                Yv = component.Y(w)
                cnodes = component.nodes
                idx1 = nodes.index(component.nodes[0])
                idx2 = nodes.index(component.nodes[1])
                Y[idx1, idx1] += Yv
                Y[idx2, idx2] += Yv
                Y[idx1, idx2] -= Yv
                Y[idx2, idx1] -= Yv

            if isinstance(component, IdealOpAmp):
                merge_node_groups(node_groups, component.nodes[2], "gnd")
                v = np.zeros(dim, dtype=complex)
                idx1 = nodes.index(component.nodes[0])
                v[idx1] = 1.0
                idx2 = nodes.index(component.nodes[1])
                v[idx2] = -1.0
                voltage_constraints.append(v)
                voltage_constraints_keys.append(None)


            if isinstance(component, IdealVoltageSource):
                merge_node_groups(node_groups, component.nodes[0], component.nodes[1])
                v = np.zeros(dim, dtype=complex)
                idx1 = nodes.index(component.nodes[0])
                v[idx1] = 1.0
                idx2 = nodes.index(component.nodes[1])
                v[idx2] = -1.0
                voltage_constraints.append(v)
                voltage_constraints_keys.append(component.name)

        voltage_constraints = np.array(voltage_constraints)
        Yiso = np.array([sum([Y[nodes.index(n)] for n in ng])
            for ng in node_groups if not "gnd" in ng])
        Yeff = np.vstack((Yiso, voltage_constraints))
        if "gnd" in nodes:
            Yeff = np.delete(Yeff, nodes.index("gnd"), 1)
            nodes.remove("gnd")

        Ykeys = [None]*len(Yiso) + voltage_constraints_keys
        sol = {}
        Zeff = np.linalg.inv(Yeff)
        for idx, key in enumerate(Ykeys):
            if key is not None:
                sol[key] = Zeff[:, idx]
        for component in self.components:
            if isinstance(component, IdealCurrentSource):
                v = np.zeros(Zeff.shape[0], dtype=complex)
                if component.nodes[0] != "gnd":
                    v += Zeff[:, [i for i, ng in enumerate(node_groups)
                        if component.nodes[0] in ng][0]]
                if component.nodes[1] != "gnd":
                    v -= Zeff[:, [i for i, ng in enumerate(node_groups)
                        if component.nodes[1] in ng][0]]
                sol[component.name] = v
        return {key: dict(zip(nodes, value))
            for key, value in sol.items()}
