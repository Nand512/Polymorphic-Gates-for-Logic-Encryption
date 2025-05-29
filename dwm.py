import replacement

def gate(info, n):
    keys = []
    info[0] = "dwm"
    info[1] = f"DWM_{n}"

    i = 0
    while i < len(info):
        if i == len(info) - 1:
            info[i] = info[i][:-2]
            info[i] = info[i] + ","
        i += 1
    
    start = (n - 1) * 3 + 1
    end = n * 3
    for num in range(start, end + 1):
        if num == end:
            info.append(f"k{num});")
        else:
            info.append(f"k{num},")

    info = " ".join(info)
    return(info)

def circuit(info, n):
    info = info.split()
    total_output = info[2][1:-1]

    end = []
    newinputs = []
    newwires = []

    keys = info[5:]
    j = 0
    while j < len(keys):
        if j == len(keys) - 1:
            keys[j] = keys[j][:-2]
        else:
            keys[j] = keys[j][:-1]
        j += 1

    info = info[:-3]
    inputs = []
    i = 3
    while i < len(info):
        if i == len(info) - 1:
            info[i] = info[i][:-1]
            info[i] = info[i] + ");"
        inputs.append(info[i])
        i += 1

    a = inputs[0][:-1]
    b = inputs[1][:-2]

    not_s0 = "not s0_DWM%d (not_s0_%d, %s);" % (n, n, keys[0])
    not_s1 = "not s1_DWM%d (not_s1_%d, %s);" % (n, n, keys[1])
    not_s2 = "not s2_DWM%d (not_s2_%d, %s);" % (n, n, keys[2])

    # This is a big 8x1 MUX, but i5 is unused/FALSE (technically 8 functions?)
    i0 = "xnor i0_DWM%d (i0_%d, %s, %s);" % (n, n, a, b) # a XNOR b
    i1 = "xor i1_DWM%d (i1_%d, %s, %s);" % (n, n, a, b) # a XOR b
    i2 = "or i2_DWM%d (i2_%d, %s, %s);" % (n, n, a, b) # a OR b
    i3 = "nor i3_DWM%d (i3_%d, %s, %s);" % (n, n, a, b) # a NOR b
    i4 = "buf i4_DWM%d (i4_%d, %s);" % (n, n, a) # NOT a
    i6 = "and i6_DWM%d (i6_%d, %s, %s);" % (n, n, a, b) # a AND b
    i7 = "nand i7_DWM%d (i7_%d, %s, %s);" % (n, n, a, b) # a NAND b
    # 8 ANDs
    and_0 = "and AND0_DWM%d (AND0_%d, i0_%d, not_s0_%d, not_s1_%d, not_s2_%d);" % (n, n, n, n, n, n)
    and_1 = "and AND1_DWM%d (AND1_%d, i1_%d, not_s0_%d, not_s1_%d, %s);" % (n, n, n, n, n, keys[2])
    and_2 = "and AND2_DWM%d (AND2_%d, i2_%d, not_s0_%d, %s, not_s2_%d);" % (n, n, n, n, keys[1], n)
    and_3 = "and AND3_DWM%d (AND3_%d, i3_%d, not_s0_%d, %s, %s);" % (n, n, n, n, keys[1], keys[2])
    and_4 = "and AND4_DWM%d (AND4_%d, i4_%d, %s, not_s1_%d, not_s2_%d);" % (n, n, n, keys[0], n, n)
    and_6 = "and AND6_DWM%d (AND6_%d, i6_%d, %s, %s, not_s2_%d);" % (n, n, n, keys[0], keys[1], n)
    and_7 = "and AND7_DWM%d (AND7_%d, i7_%d, %s, %s, %s);" % (n, n, n, keys[0], keys[1], keys[2])
    # AND outputs go into OR gate, output is total output
    final_output = "or OR_DWM%d (%s, AND0_%d, AND1_%d, AND2_%d, AND3_%d, AND4_%d, AND6_%d, AND7_%d);" % (n, total_output, n, n, n, n, n, n, n)

    newinputs.append(keys)
    newwires.append("not_s0_%d,not_s1_%d,not_s2_%d,i0_%d,i1_%d,i2_%d,i3_%d,i4_%d,i6_%d,i7_%d,AND0_%d,AND1_%d,AND2_%d,AND3_%d,AND4_%d,AND6_%d,AND7_%d" % (n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n))

    end.extend((not_s0, not_s1, not_s2, i0, i1, i2, i3, i4, i6, i7, and_0, and_1, and_2, and_3, and_4, and_6, and_7, final_output))

    return (end, newinputs, newwires)