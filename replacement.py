import signal_selection
import key_distribution

def make_file(l):
    newfile = "output.v"

    with open(newfile, "w") as file:
        for line in l:
            file.write(f"{line}\n")

def replace(netlist, polymorphic_gate):
    if polymorphic_gate == "GSHE":
        import GSHE as g
    '''
    elif polymorphic_gate == "memristorCMOS":
        import mem as g
    etc etc
    '''
    G, primary_inputs, primary_outputs = signal_selection.build_graph(netlist)
    selected_gates = signal_selection.select_gates(G, primary_outputs, n=45)
    s1, s2, s3 = key_distribution.distribute_keys(k=60, l=16, n=45) # k = 60 from Hybrid Shielding; GSHE = 16 functions (l)
    keys = []

    i = 0
    while i < s2: # adds key inputs to the list "keys"
        keys.append(f"k{i}")
        i += 1

    netlist = open(netlist)
    newfile = []
    j = 1
    for line in netlist:
        if len(line.split()) > 1:
            line = line.split()
            if line[1] in selected_gates:
                new = g.mux(g.gate(line, j), j)
                for n in new:
                    newfile.append(n)
                j += 1
            else:
                newfile.append(" ".join(line))
    
    make_file(newfile)