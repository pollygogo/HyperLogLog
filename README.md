# HyperLogLog

A lightweight and customizable Python implementation of the HyperLogLog algorithm for estimating cardinality with minimal memory usage.

---

## Features

- Uses `mmh3` to generate 64-bit hash values
- Compact registers using `bitarray` (6 bits per register)
- Adjustable:
  - Number of values to insert
  - Range of input values (affects uniqueness)
  - Target error rate
- Compares HyperLogLog to Python’s built-in `set` in terms of accuracy and memory usage

---

## Clone the repository

```
git clone https://github.com/yourusername/hyperloglog.git
cd hyperloglog
```
## Install dependencies
```
pip install -r requirements.txt
```
## Run the script
```
python main.py
```

---

## Sample Output
```
Inserted values : 100,000
Target error rate: 2.00%

Method                    Count    Size (bytes)
-----------------------------------------------
HyperLogLog           43,987.08           3,152
Exact Set                43,170       2,097,368
```
