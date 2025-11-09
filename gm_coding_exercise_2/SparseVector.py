#!/usr/bin/env python

class SparseVector:
  sparse_vector = {}
  def __init__(self, vector):
    self.sparse_vector = {}
    for idx in range(len(vector)):
      if not vector[idx] == 0:
        self.sparse_vector.update({idx: vector[idx]})
    print(self.sparse_vector)
    self.max_length = len(vector)

  def dot_product(self, other):
    min_len = min(self.max_length, other.max_length)
    product = 0
    for i in range(min_len):
      a = self.sparse_vector.get(i)
      b = other.sparse_vector.get(i)
      if not a is None and not b is None:
        product += a * b

    return product

if __name__ == "__main__":
    sv = SparseVector([3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 7, 8, 0, 0, 0, 0, 0])
    print(sv.dot_product(SparseVector([1])))
