import sys
sys.path.append('.')
from SparseVector import SparseVector

def test_1():
    sv = SparseVector([8, 0, 0, 0, 0, 4, 0, 3])
    p = sv.dot_product(SparseVector([0, 0, 0, 1, 6, 1, 0, 15]))
    assert p == 49, f"Expecting response: 49, got: {p}"
