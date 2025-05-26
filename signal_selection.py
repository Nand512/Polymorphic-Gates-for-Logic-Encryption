import networkx as nx
import matplotlib.pyplot as plt

def parse(netlist):
    inputs = set()
    outputs = set()
    wires = set()
    gates = []
    keywords = ["and", "nand", "or", "nor", "not", "xor", "xnor", "buf"]
    key = 0
    netlist = open(netlist)
    for line in netlist:
        if len(line.split()) > 0:
            line = line.split()
            if line[0] == "input":
                key = 1
                for gate in line[1][:-1].split(","):
                    inputs.add(gate)
            if line[0] == "output":
                key = 2
                for gate in line[1][:-1].split(","):
                    outputs.add(gate)
            if line[0] == "wire":
                key = 3
                for gate in line[1][:-1].split(","):
                    wires.add(gate)
            if line[0] in keywords:
                key = 4
            if key == 1 and line[0] != "input":
                for gate in line:
                    gate = gate[:-1].split(",")
                    for i in gate:
                        inputs.add(i)
            if key == 2 and line[0] != "output":
                for gate in line:
                    gate = gate[:-1].split(",")
                    for i in gate:
                        outputs.add(i)
            if key == 3 and line[0] != "wire":
                for gate in line:
                    gate = gate[:-1].split(",")
                    for i in gate:
                        wires.add(i)
            if key == 4 and len(line) == 5: # Ensures gates selected have exactly 2 inputs
                info = []  # [type, name, output, inputs]
                g = []
                i = 0
                while i < len(line):
                    if i == 0:
                        info.append(line[0])  # gate type
                    elif i == 1:
                        info.append(line[1])  # gate name
                    elif i == 2:
                        info.append(line[2].replace("(", "").replace(",", ""))  # output
                    else:
                        g.append(line[i].replace("(", "").replace(",", "").replace(";", "").replace(")", ""))
                    i += 1
                info.append(g)
                gates.append(info)
    return inputs, outputs, wires, gates

def build_graph(netlist):
    inputs, outputs, wires, gates = parse(netlist)
    G = nx.DiGraph()

    # Label primary inputs/outputs
    for pi in inputs:
        G.add_node(pi, type="PI")
    for po in outputs:
        G.add_node(po, type="PO")

    # Label wires
    for wire in wires:
        G.add_node(wire, type="wire")  # Explicit wire tag

    # Add gates and connections
    for gate in gates:
        gate_type, gate_name, gate_output, gate_inputs = gate
        G.add_node(gate_name, type=gate_type.lower())  # Ensure lowercase consistency
        G.add_edge(gate_name, gate_output)
        for input_wire in gate_inputs:
            G.add_edge(input_wire, gate_name)

    return G, inputs, outputs

def compute_weights(G, primary_outputs):
    weights = {}
    po_paths = {po: set(nx.ancestors(G, po)) for po in primary_outputs}  # Precompute paths
    for node in G.nodes():
        node_type = G.nodes[node].get('type')
        if node_type not in ['PI', 'PO', 'wire']:  # Skip I/Os and wires
            weights[node] = sum(1 for po in primary_outputs if node in po_paths[po])
    return weights

def estimate_stability(G, node, primary_outputs):
    gate_type = G.nodes[node].get('type')
    try:
        depth = nx.shortest_path_length(G, node, next(iter(primary_outputs)))
    except nx.NetworkXNoPath:
        return 0.0  # Assign lowest stability if no path exists

    if gate_type in ['and', 'or', 'nand', 'nor', 'buf']:
        stability = 0.7
    elif gate_type in ['xor', 'xnor']:
        stability = 0.3
    else:
        stability = 0.5
    return stability * (1 / (1 + 0.1 * depth))

def select_gates(G, primary_outputs, n=45):
    weights = compute_weights(G, primary_outputs)
    stabilities = {
        node: estimate_stability(G, node, primary_outputs)
        for node in G.nodes()
        if G.nodes[node].get('type') not in ['PI', 'PO', 'wire']  # Explicitly exclude wires
    }
    ranked = sorted(
        [(node, stabilities[node], weights[node]) for node in stabilities.keys()],
        key=lambda x: (-x[1], -x[2])  # Sort by stability (desc), then weight (desc)
    )
    return [gate[0] for gate in ranked[:n]]

def visualize_graph(G, selected_gates, primary_inputs, primary_outputs):
    node_colors = []
    for node in G.nodes():
        if node in selected_gates:
            node_colors.append('red')    # Selected gates
        elif node in primary_inputs:
            node_colors.append('green')  # Primary inputs
        elif node in primary_outputs:
            node_colors.append('blue')   # Primary outputs
        else:
            node_colors.append('lightgray')  # Other nodes
    nx.draw(G, with_labels=True, node_color=node_colors, node_size=500)
    plt.title("Selected Gates for Hybrid Shielding (Red)")
    plt.show()