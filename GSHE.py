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