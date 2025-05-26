import replacement

def gate(info, n):
    keys = []
    info[0] = "gshe"
    info[1] = f"GSHE_{n}"

    i = 0
    while i < len(info):
        if i == len(info) - 1:
            info[i] = info[i][:-2]
            info[i] = info[i] + ","
        i += 1
    
    start = (n - 1) * 8 + 1
    end = n * 8
    for num in range(start, end + 1):
        if num == end:
            info.append(f"k{num});")
        else:
            info.append(f"k{num},")

    info = " ".join(info)
    return(info)

def mux(info, n):
    info = info.split()
    total_output = info[2][1:-1]

    end = []

    keys = info[5:]
    j = 0
    while j < len(keys):
        if j == len(keys) - 1:
            keys[j] = keys[j][:-2]
        else:
            keys[j] = keys[j][:-1]
        j += 1

    info = info[:-8]

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

    # This is the first of 5 4x1 MUXs used to create a 16x1 MUX
    i0 = "nand i0_GSHE%d (i0_%d, %s, %s);" % (n, n, a, b) # a NAND b
    i1 = "and i1_GSHE%d (i1_%d, %s, %s);" % (n, n, a, b) # a AND b
    i2 = "nor i2_GSHE%d (i2_%d, %s, %s);" % (n, n, a, b) # a NOR b
    i3 = "or i3_GSHE%d (i3_%d, %s, %s);" % (n, n, a, b) # a OR b
    # Would be easier with key sharing to be honest...
    not_s0 = "not s0_GSHE%d (not_s0_%d, %s);" % (n, n, keys[0])
    not_s1 = "not s1_GSHE%d (not_s1_%d, %s);" % (n, n, keys[1])
    # 4 ANDs, ANDing s0/s1, i0-i3, etc.
    and_0_M0 = "and AND0_M0_GSHE%d (AND0_M0_%d, not_s0_%d, i0_%d, not_s1_%d);" % (n, n, n, n, n)
    and_1_M0 = "and AND1_M0_GSHE%d (AND1_M0_%d, not_s0_%d, i1_%d, %s);" % (n, n, n, n, keys[1])
    and_2_M0 = "and AND2_M0_GSHE%d (AND2_M0_%d, %s, i2_%d, not_s1_%d);" % (n, n, keys[0], n, n)
    and_3_M0 = "and AND3_M0_GSHE%d (AND3_M0_%d, %s, i3_%d, %s);" % (n, n, keys[0], n, keys[1])
    # AND outputs go into OR gate, output goes into 5th 4x1 MUX to create 16x1 MUX
    or_M0 = "or OR_M0_GSHE%d (M0_OUT_%d, AND0_M0_%d, AND1_M0_%d, AND2_M0_%d, AND3_M0_%d);" % (n, n, n, n, n, n)

    # This is the second of 5 4x1 MUXs used to create a 16x1 MUX
    i4 = "xnor i4_GSHE%d (i4_%d, %s, %s);" % (n, n, a, b) # a XNOR b
    i5 = "xor i5_GSHE%d (i5_%d, %s, %s);" % (n, n, a, b) # a XOR b
    i6 = "not i6_GSHE%d (i6_%d, %s);" % (n, n, a) # NOT a
    i7 = "buf i7_GSHE%d (i7_%d, %s);" % (n, n, a) # BUF a
    # 4 ANDs, ANDing s0/s1, i4-i7, etc.
    and_0_M1 = "and AND0_M1_GSHE%d (AND0_M1_%d, not_s0_%d, i4_%d, not_s1_%d);" % (n, n, n, n, n)
    and_1_M1 = "and AND1_M1_GSHE%d (AND1_M1_%d, not_s0_%d, i5_%d, %s);" % (n, n, n, n, keys[1])
    and_2_M1 = "and AND2_M1_GSHE%d (AND2_M1_%d, %s, i6_%d, not_s1_%d);" % (n, n, keys[0], n, n)
    and_3_M1 = "and AND3_M1_GSHE%d (AND3_M1_%d, %s, i7_%d, %s);" % (n, n, keys[0], n, keys[1])
    # AND outputs go into OR gate, output goes into 5th 4x1 MUX to create 16x1 MUX
    or_M1 = "or OR_M1_GSHE%d (M1_OUT_%d, AND0_M1_%d, AND1_M1_%d, AND2_M1_%d, AND3_M1_%d);" % (n, n, n, n, n, n)

    # This is the third of 5 4x1 MUXs used to create a 16x1 MUX
    i8 = "not i8_GSHE%d (i8_%d, %s);" % (n, n, b) # NOT b
    i9 = "buf i9_GSHE%d (i9_%d, %s);" % (n, n, b) # BUF b
    i10 = "and i10_GSHE%d (i10_%d, %s, i8_%d);" % (n, n, a, n) # a AND NOT b
    i11 = "and i11_GSHE%d (i11_%d, i6_%d, %s);" % (n, n, n, b) # NOT a AND b
    # 4 ANDs, ANDing s0/s1, i8-i11, etc.
    and_0_M2 = "and AND0_M2_GSHE%d (AND0_M2_%d, not_s0_%d, i8_%d, not_s1_%d);" % (n, n, n, n, n)
    and_1_M2 = "and AND1_M2_GSHE%d (AND1_M2_%d, not_s0_%d, i9_%d, %s);" % (n, n, n, n, keys[1])
    and_2_M2 = "and AND2_M2_GSHE%d (AND2_M2_%d, %s, i10_%d, not_s1_%d);" % (n, n, keys[0], n, n)
    and_3_M2 = "and AND3_M2_GSHE%d (AND3_M2_%d, %s, i11_%d, %s);" % (n, n, keys[0], n, keys[1])
    # AND outputs go into OR gate, output goes into 5th 4x1 MUX to create 16x1 MUX
    or_M2 = "or OR_M2_GSHE%d (M2_OUT_%d, AND0_M2_%d, AND1_M2_%d, AND2_M2_%d, AND3_M2_%d);" % (n, n, n, n, n, n)

    # This is the fourth of 5 4x1 MUXs used to create a 16x1 MUX
    i12 = "or i12_GSHE%d (i12_%d, %s, i8_%d);" % (n, n, a, n) # a OR NOT b
    i13 = "or i13_GSHE%d (i13_%d, i6_%d, %s);" % (n, n, n, b) # NOT a OR b
    i14 = "buf i14_GSHE%d (i14_%d, 1'b1);" % (n, n) # TRUE
    i15 = "buf i15_GSHE%d (i15_%d, 1'b0);" % (n, n) # FALSE
    # 4 ANDs, ANDing s0/s1, i0-i3, etc.
    and_0_M3 = "and AND0_M3_GSHE%d (AND0_M3_%d, not_s0_%d, i12_%d, not_s1_%d);" % (n, n, n, n, n)
    and_1_M3 = "and AND1_M3_GSHE%d (AND1_M3_%d, not_s0_%d, i13_%d, %s);" % (n, n, n, n, keys[1])
    and_2_M3 = "and AND2_M3_GSHE%d (AND2_M3_%d, %s, i14_%d, not_s1_%d);" % (n, n, keys[0], n, n)
    and_3_M3 = "and AND3_M3_GSHE%d (AND3_M3_%d, %s, i15_%d, %s);" % (n, n, keys[0], n, keys[1])
    # AND outputs go into OR gate, output goes into 5th 4x1 MUX to create 16x1 MUX
    or_M3 = "or OR_M3_GSHE%d (M3_OUT_%d, AND0_M3_%d, AND1_M3_%d, AND2_M3_%d, AND3_M3_%d);" % (n, n, n, n, n, n)

    # This is the fifth of 5 4x1 MUXs used to create a 16x1 MUX
    not_s2 = "not s2_GSHE%d (not_s2_%d, %s);" % (n, n, keys[2])
    not_s3 = "not s3_GSHE%d (not_s3_%d, %s);" % (n, n, keys[3])
    # 4 ANDs, ANDing s3/s4, outputs from other 4 MUXs, etc.
    and_0_M4 = "and AND0_M4_GSHE%d (AND0_M3_%d, not_s2_%d, M0_OUT_%d, not_s3_%d);" % (n, n, n, n, n)
    and_1_M4 = "and AND1_M4_GSHE%d (AND1_M3_%d, not_s2_%d, M1_OUT_%d, %s);" % (n, n, n, n, keys[3])
    and_2_M4 = "and AND2_M4_GSHE%d (AND2_M3_%d, %s, M2_OUT_%d, not_s3_%d);" % (n, n, keys[2], n, n)
    and_3_M4 = "and AND3_M4_GSHE%d (AND3_M3_%d, %s, M3_OUT_%d, %s);" % (n, n, keys[2], n, keys[3])
    # AND outputs go into OR gate, output is final output
    final_output = "or GSHE%d_OUT (%s, AND0_M4_%d, AND1_M4_%d, AND2_M4_%d, AND3_M4_%d);" % (n, total_output, n, n, n, n)

    end.extend((i0, i1, i2, i3, not_s0, not_s1, and_0_M0, and_1_M0, and_2_M0, and_3_M0, or_M0, i4, i5, i6, i7,\
               and_0_M1, and_1_M1, and_2_M1, and_3_M1, or_M1, i8, i9, i10, i11, and_0_M2, and_1_M2, and_2_M2, and_3_M2, or_M2,\
                i12, i13, i14, i15, and_0_M3, and_1_M3, and_2_M3, and_3_M3, or_M3, not_s2, not_s3, and_0_M4, and_1_M4, and_2_M4, and_3_M4, final_output))

    return end