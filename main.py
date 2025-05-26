import signal_selection
import key_distribution
import replacement

netlist = "c880.v"

G, primary_inputs, primary_outputs = signal_selection.build_graph(netlist)
selected_gates = signal_selection.select_gates(G, primary_outputs, n=45)

# signal_selection.visualize_graph(G, selected_gates, primary_inputs, primary_outputs)

s1, s2, s3 = key_distribution.distribute_keys(k=60, l=16, n=45) # k = 60 from Hybrid Shielding; GSHE = 16 functions (l)

replacement.replace(netlist, "GSHE")