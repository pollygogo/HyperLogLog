from mmh3 import hash64
from math import log, log2, ceil
from bitarray import bitarray

def hash_value(value):
    """
    Compute the hash value of a given value.
    """
    # Use mmh3 to compute the hash value
    h = hash64(str(value))
    return h[0] & 0xFFFFFFFFFFFFFFFF
    # Ensure the hash value is unsigned 64 bits

def compute_m (error_rate):
    """
    Compute the number of registers needed for a given error rate.
    """
    raw_m = (1.04 / error_rate) ** 2
    return 1 << (ceil(log2(raw_m))) # round up to the next power of 2

def compute_p(m):
    """
    Compute the number of bits needed to represent m.
    """
    return int(log2(m)) # number of bits needed to represent m


def create_hyperloglog(error_rate):
    """
    Create a HyperLogLog data structure with the given error rate.
    Buckets are represented as a contiguous array of bits.
    """
    m = compute_m(error_rate)
    bits_per_bucket = 6
    total_bits = m * bits_per_bucket
    hll = bitarray(total_bits)
    hll.setall(0)
    return hll, m, bits_per_bucket

def get_bucket_index(h, p):
    """
    Get the index of the bucket for a given hash value.
    """
    bucket = h >> (64 - p)
    return bucket

def get_leading_zero_count(h, p):
    """
    Given a 64-bit hash value and the number of bucket bits p,
    return the position of the first 1 in the remaining (64 - p) bits.
    This is equivalent to counting the number of leading zeros, then adding 1.
    """
    tail = h & ((1 << (64 - p)) - 1)  # mask to keep lower (64 - p) bits
    if tail == 0:
        return 64 - p  # all bits zero => max leading zero count
    return (64 - p) - tail.bit_length() + 1

def get_bucket(hll, bucket_index, bits_per_bucket):
    """
    Read the value of the bucket at the given bucket index.
    """
    start = bucket_index * bits_per_bucket
    end = start + bits_per_bucket
    return int(hll[start:end].to01(), 2)

def set_bucket(hll, index, value, bits_per_bucket):
    """
    Set the value of the bucket at the given index.
    """
    start = index * bits_per_bucket
    bin_value = bin(value)[2:].zfill(bits_per_bucket)
    for i in range(bits_per_bucket):
        hll[start + i] = int(bin_value[i])


def add_value(hll, value, p, bits_per_bucket):
    h = hash_value(value)
    bucket = get_bucket_index(h, p)
    leading_zeroes = get_leading_zero_count(h, p)
    current_val = get_bucket(hll, bucket, bits_per_bucket)
    if leading_zeroes > current_val:
        set_bucket(hll, bucket, leading_zeroes, bits_per_bucket)

def estimate_cardinality(hll, m, bits_per_bucket):
    """
    Estimate the cardinality of the HyperLogLog data structure.
    """
    z = 0
    V = 0
    # Iterate over all buckets
    for i in range(m):
        reg = get_bucket(hll, i, bits_per_bucket)
        z += 2 ** -reg # compute the sum of 2^-reg where reg is the max leading zero count in the bucket
        if reg == 0:
            V += 1 # Count empty buckets

    # cardinality = bias_correction_constant * m * harmonic_mean_of_leading_zero_counts     
    raw_E = 0.72134 * m * (m / z) # Raw estimate of cardinality

    # Small range correction
    if raw_E <= (5 / 2) * m:
        if V > 0:
            return m * log(m / V)
        else:
            return raw_E

    # Large range correction
    elif raw_E > (1 / 30) * (2 ** 64):
        return -(2 ** 64) * log(1 - (raw_E / 2 ** 64))

    # No correction needed
    else:
        return raw_E


