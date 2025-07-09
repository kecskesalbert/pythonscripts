# Note: run pytest from this directory

import sys
sys.path.append('.')
from graph import Graph

def test_1():
    graph = Graph()
    count = graph.count_connected(7, [[0, 1], [1, 2], [1, 3], [2, 4], [5, 6]]) 
    assert count == 2, f"Expecting response: 2, got: {count}"


def test_2():
    graph = Graph()
    count = graph.count_connected(7, [[0, 1], [0, 2], [3, 4], [5, 6]]) 
    assert count == 3, f"Expecting response: 3, got: {count}"


def test_3():
    graph = Graph()
    count = graph.count_connected(5, [[0, 4], [4, 2], [2, 3], [3, 1]]) 
    assert count == 1, f"Expecting response: 1, got: {count}"


def test_4():
    graph = Graph()
    count = graph.count_connected(10, [[0, 1], [7, 8], [3, 9], [5, 6], [2, 4], [1, 3], [7, 1], [6, 2]])
    assert count == 2, f"Expecting response: 2, got: {count}"

def test_5():
    graph = Graph()
    count = graph.count_connected(5, [])
    assert count == 0, f"Expecting response: 0, got: {count}"

def test_6():
    graph = Graph()
    count = graph.count_connected(7, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]])
    assert count == 1, f"Expecting response: 1, got: {count}"

def test_7():
    graph = Graph()
    count = graph.count_connected(12, [[0, 1], [1, 4], [4, 3], [3, 0], [2, 5], [6, 9], [7, 8], [8, 11], [11, 10], [10, 7]])
    assert count == 4, f"Expecting response: 4, got: {count}"
