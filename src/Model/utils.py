import numpy as np

def r(n=6):
    return np.random.randint(1,n+1)

def reroll(prob):
    if prob < 0 or prob > 1:
        raise ValueError("Out of bounds")
    return prob + (1-prob) * prob

def rr1(prob):
    if prob < 0 or prob > 1:
        raise ValueError("Out of bounds")
    if prob > 6/7:
        return 1
    return prob + prob/6