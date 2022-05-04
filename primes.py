from numpy.core.arrayprint import array2string
from copy import deepcopy
import numpy as np
import random


def mutate(m: np.array) -> np.array:
    '''
    Randomly slightly mutates an image array 
    '''
    shape = m.shape
    for x in range(1, shape[0] - 1):
        for y in range(1, shape[1] - 1):
            r = random.randint(0, 800)
            if r == 0:
                m[x][y] = m[x + 1][y]
            if r == 1:
                m[x][y] = m[x - 1][y]
            if r == 2:
                m[x][y] = m[x][y + 1]
            if r == 3:
                m[x][y] = m[x][y - 1]
    return m


def load_primes() -> list[int]:
    '''
    Loads the first 2000 prime numbers from a file
    '''

    with open('primes.txt') as file:
        return [int(n) for n in file.readline().rstrip().split(' ')]


def array_to_string(m: np.array) -> str:
    '''
    Converts a number array to string value
    '''

    flattened = array2string(m.flatten(), separator='',
                             edgeitems=100000000)[1:-1].replace('\n ', '')
    return flattened


def to_digit(n: int) -> int:
    ''' 
    Converts a grayscale colour value to a digit ranked on density
    '''
    return [1, 4, 7, 6, 9, 2, 3, 5,  0, 8][np.int((n / 255) * 9)]


def generate_possible_primes(image: np.array, amount: int, existing=set()) -> list[str]:
    '''
    Generates specified amount of distinct mutations not divisible by first 2000 primes
    '''

    primes = load_primes()
    possible_primes = {array_to_string(image), }.union(existing)
    while len(possible_primes) < amount:
        num = array_to_string(mutate(deepcopy(image)))
        num = patch_prime(num)
        if prime_quick_check(int(num), primes):
            possible_primes.add((num))
    return list(possible_primes)


def prime_quick_check(possible: int, primes: list[int]) -> bool:
    '''
    Checks if number is divible by any of first 2000 primes
    '''

    for prime in primes:
        if possible % prime == 0:
            return False
    return True


def patch_prime(n: str) -> str:
    '''
    Fixes numbers that could never be prime
    '''

    if n[-1] == '4' or n[-1] == '6':
        n = n[:-1] + '7'
    if n[-1] == '2' or n[-1] == '5':
        n = n[:-1] + '3'
    if n[-1] == '0' or n[-1] == '8':
        n = n[:-1] + '5'

    return n
