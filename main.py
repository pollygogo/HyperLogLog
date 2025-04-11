import hyperloglog
from random import randint
from sys import getsizeof

def main():
    """
    Compare the memory usage and cardinality estimation of HyperLogLog and a set.
    """

    # You can change the number of random values and the maximum value for random integers here to test the performance with different parameters.
    n = 100000  # Number of random values to add
    max_value = 50000 # Maximum value for random integers

    # You can change the error rate of the HyperLogLog here.
    error_rate = 0.02 # Lower error rate means more memory usage

    set_of_values = set()
    hll, m, bits_per_bucket = hyperloglog.create_hyperloglog(error_rate)
    p = hyperloglog.compute_p(m)

    for i in range(n):
        value = randint(1, max_value)
        hyperloglog.add_value(hll,value, p, bits_per_bucket)
        set_of_values.add(value)

    hll_count = hyperloglog.estimate_cardinality(hll, m, bits_per_bucket)
    set_count = len(set_of_values)

    hll_size = getsizeof(hll)
    set_size = getsizeof(set_of_values)

    # Print the results
    print(f"Inserted values : {n:,}")
    print(f"Target error rate: {error_rate:.2%}")
    print()
    print(f"{'Method':<15} {'Count':>15} {'Size (bytes)':>15}")
    print("-" * 47)
    print(f"{'HyperLogLog':<15} {hll_count:>15,.2f} {hll_size:>15,}")
    print(f"{'Exact Set':<15} {set_count:>15,} {set_size:>15,}")

if __name__ == "__main__":
    main()        