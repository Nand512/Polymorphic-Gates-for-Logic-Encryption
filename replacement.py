import signal_selection
import key_distribution

def make_file(l, newinputs, newwires, output):
    newfile = "%s" % output
    with open(newfile, "w") as file:
        k = 0
        gatelist = ["and", "or", "nand", "nor", "not", "buf", "xor", "xnor"]
        for line in l:
            s = line.split()
            if len(s) > 0:
                if s[0] == "module":
                    file.write("%s%s,\n" % (line, ",".join(newinputs[0])))
                    i = 1
                    while i < len(newinputs):
                        file.write("\t\t\t%s,\n" % (",".join(newinputs[i])))
                        i += 1
                elif s[0] == "input":
                    file.write("%s%s,\n" % (line, ",".join(newinputs[0])))
                    i = 1
                    while i < len(newinputs):
                        file.write("\t\t\t%s,\n" % (",".join(newinputs[i])))
                        i += 1
                elif s[0] == "wire":
                    file.write(f"{line}\n")

                    smaller_lists = []
                    for i in range(0, len(newwires), 10):
                        smaller_lists.append(newwires[i:i+10])
                    
                    i = 0
                    while i < len(smaller_lists):
                        file.write("\t\t\t%s,\n" % (",".join(smaller_lists[i])))
                        i += 1
                elif s[0] == "endmodule":
                    file.write(f"\n{line}")
                else:
                    file.write(f"{line}\n")
    
    print("File done!")

def replace(netlist, polymorphic_gate, output):
    if polymorphic_gate == "GSHE": # imports gshe.py, the python file for GSHE switch (16 boolean functions)
        import GSHE as g
    elif polymorphic_gate == "DWM": # imports dwm.py, the python file for 5-Terminal Magnetic DWM (7 boolean functions)
        import dwm as g
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
    newinputs = []
    j = 1
    for line in netlist:
        if len(line.split()) > 1:
            line = line.split()
            if line[1] in selected_gates:
                new = g.circuit(g.gate(line, j), j)
                newinputs.extend(new[1])
                for n in new[0]:
                    newfile.append(n)
                j += 1
            else:
                newfile.append(" ".join(line))
        else:
            newfile.append("".join(line))

    make_file(newfile, newinputs, new[2][0].split(","), output)