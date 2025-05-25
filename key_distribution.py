import math

def distribute_keys(k, l, n):
    s1_size = 2 * math.log2(l) # Reinstate Block
    s2_size = n # SAT-Resilient Block
    s3_size = k - (s1_size + s2_size) # Internal State Block
    return int(s1_size), int(s2_size), int(s3_size)