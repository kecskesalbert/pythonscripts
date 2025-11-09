#!/usr/bin/env python

# https://www.w3resource.com/python-exercises/list/

# Sum all the items in a list
def exercise_1(args):
    sum = 0
    for a in args:
        sum += a
    print(f"Sum: {sum}")

# Multiply all the items in a list
def exercise_2(args):
    prod = 1
    for a in args:
        prod = prod * a
    print(f"Product: {prod}")

# Get the largest number from a list
def exercise_3(args):
    largest = None
    for a in args:
        if largest is None or a > largest:
            largest = a
    print(f"Largest: {largest}")

# Get the smallest number from a list
def exercise_4(args):
    smallest = None
    for a in args:
        if smallest is None or a < smallest:
            smallest = a
    print(f"Smallest: {smallest}")

# Remove duplicates from a list
def exercise_7(args):
    count = {}
    for a in args:
        if count.get(a):
            count[a] += 1
        else:
            count[a] = 1
    print(f"{[ c for c in count ]}")
        
# Remove the 0th, 4th and 5th elements
def exercise_12(args):
    try:
        args.pop(5)
    except IndexError:
        pass
    try:
        args.pop(4)
    except IndexError:
        pass
    try:
        args.pop(0)
    except IndexError:
        pass
    print(f"After 1st, 5th, 6th elements removed: {args}")

# Remove even numbers from the list
def exercise_14(args):
    x = []
    for a in args:
        if a/2 != int(a/2):
            x.append(a)
    print(f"Without even numbers: {x}")

# Shuffle list
def exercise_15(args):
    import random
    random.shuffle(args)
    print(f"Shuffled: {args}")

# Check if all numbers are prime
def exercise_17(args):
    import math
    largest = None
    for a in args:
        if largest is None or a > largest:
            largest = a
    primes = [ 1 ]
    for n in range(2, largest+1):
        is_prime = True
        for t in range(2, int(math.sqrt(n))+1):
            if n/t == int(n/t):
                is_prime = False
                break
        if is_prime:
            primes.append(n)
    prime_count = 0
    for a in args:
        if a in primes:
            prime_count += 1
    print("primes={}, prime_count={}, all_primes={}".format(
            primes,
            prime_count,
            prime_count==len(args)))

# Generate all permutations of a list
def exercise_18(args):
    gen = []
    def permutate(mem,l):
        for idx in range(len(l)):
            head = l[idx]
            tail = l[:idx] + l[idx+1:]
            # print(f"mem={mem}, Head={head}, tail={tail}")
            if len(tail) == 1:
                gen.append( mem + [ head ] + tail )
            else:
                permutate(mem + [ head ],tail)
    permutate([],args)
    for g in gen:
        print(g)

# Find the second smallest number in a list
def exercise_27(args):
    args.sort()
    print(f"Second smallest: {args[1]}")

# Find the second largest number in a list
def exercise_28(args):
    args.sort()
    print(f"Second largest: {args[-2]}")

# Get unique values from a list
def exercise_29(args):
    h = {}
    for a in args:
        h[a] = 1
    print(list(h.keys()))

# Get the frequency of elements in a list
def exercise_30(args):
    h = {}
    for a in args:
        if h.get(a):
            h[a] += 1
        else:
            h[a] = 1
    print(h)

# Generate all sublists of a list
# Sublist: all permutations of length >=0 and original length (inclusive)
# TODO: this is incomplete. Need to use combination for the list items
def exercise_33(args):
    
    def permutate(cache, mem, l):
        for idx in range(len(l)):
            head = l[idx]
            tail = l[:idx] + l[idx+1:]
            if len(tail) == 1:
                cache.append(mem + [ head ] + tail)
            elif len(tail) == 0:
                cache.append(mem + [ head ])
            else:
                permutate(cache, mem + [ head ], tail)

    gen = []
    gen.append([])
    for l in range(len(args)):
        print(l, args[:l+1])
        permutate(gen, [], args[:l+1])

    for g in gen:
        print(g)

# Use the Sieve of Eratosthenes method to compute prime numbers up to a specified number
def exercise_34(args):
    import math
    up_to = args[0]
    prime = [ a for a in range(1,up_to+1) ]
    for n in range(2, int(math.sqrt(up_to))+1):
        for p in prime:
            if p!=n and p/n == int(p/n):
                prime.remove(p)
    print(f"Prime numbers up to {up_to}: {prime}")
    
# Move all zero digits to the end of a given list of numbers
def exercise_65(args):
    lastpos = len(args)-1
    for idx in range(len(args)):
        if idx >= lastpos:
            break
        if args[idx] == 0:
            args[idx] = args[lastpos]
            args[lastpos] = 0
            lastpos -= 1
    print(f"Zeros at the end: {args}")

# Rotate a list by a specified number of items to the right or left
# Last element is the rotation: + -> right, - -> left
def exercise_109(args):
    rotate_by = int(args.pop())
    l = list(args)
    if len(l) != 0:
        rotate_by = rotate_by % len(l)
    if rotate_by > 0:
        l = l[len(l)-rotate_by:] + l[:len(l)-rotate_by]
    else:
        l = l[-rotate_by:] + l[:-rotate_by]
    print(f"Rotate {rotate_by}: {l}")

# Mean
def exercise_mean(args):
    sum = 0
    for a in args:
        sum += a
    mean = None
    if len(args) > 0:
        mean = sum / len(args)
    print(f"Mean: {mean}")

# Median
def exercise_median(args):
    args.sort()
    median = None
    if len(args) > 0:
        idx = int((len(args)-1)/2)
        if len(args) % 2 == 0:
            median = (args[idx] + args[idx+1]) / 2
        else:
            median = args[idx]
    print(f"Median: {median}")

# Standard deviation
def exercise_stdev(args):
    if len(args) == 0:
        print("0 elements passed")
        return
    sum = 0
    for a in args:
        sum += a
    mean = sum / len(args)
    dev = 0
    for a in args:
        dev += (a-mean)**2
    variance = dev / len(args)
    stdev = variance**0.5
    print("Mean: {}, variance: {}, stdev: {}".format(
        mean, variance, stdev))


import sys
import random
if __name__ == "__main__":
    exercise_nr = sys.argv[1]
    params = [ int(a) if a.isnumeric() else a for a in sys.argv[2:] ]
    if len(params) == 0:
        params = [ random.randint(-5,12) for r in range(random.randint(3, 8))]
    print(f"Exercise {exercise_nr} with params: {params}")
    ret = globals()["exercise_"+exercise_nr](params)