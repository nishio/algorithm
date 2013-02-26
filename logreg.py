# -*- coding: utf-8 -*-
"""
logistic regression with regularization

>>> phi = array([
...     [1, 1, 0, 0],
...     [1, 0, 1, 0],
...     [1, 0, 0, 1],
...     [1, 1, 0, 0],
...     [1, 0, 1, 0],
...     [1, 0, 0, 1],
...     [1, 1, 0, 0],
...     [1, 0, 1, 0],
...     [1, 0, 0, 1],
...     ])

>>> vec_t = array(
...     [1, 0, 1, 0, 0, 1, 1, 0, 1])

>>> weight = learn((phi, vec_t), 1000)
>>> weight
array([ 0.13092266,  0.23127966, -0.9304073 ,  0.8300503 ])

The result suggest 'when feature[2] = 1, t will be 0' etc.


>>> for p, t in zip(phi, vec_t):
...     print_result(p, weight, t)
p=0.59 +:+ OK
p=0.31 -:- OK
p=0.72 +:+ OK
p=0.59 +:- NG
p=0.31 -:- OK
p=0.72 +:+ OK
p=0.59 +:+ OK
p=0.31 -:- OK
p=0.72 +:+ OK

>>> phi = array([
...     [1, 1],
...     [1, 0],
...     [0, 1],
...     [0, 0],
...     ])

>>> vec_t = array(
...     [1, 0, 0, 1])

>>> weight = learn((phi, vec_t), 1000)
>>> for p, t in zip(phi, vec_t):
...     print_result(p, weight, t)
p=0.50 0:+ NG
p=0.50 0:- NG
p=0.50 0:- NG
p=0.50 0:+ NG

>>> phi = array([
...     [1, 1, 1, 0],
...     [1, 0, 0, 0],
...     [0, 1, 0, 0],
...     [0, 0, 0, 1],
...     ])

>>> vec_t = array(
...     [1, 0, 0, 1])

>>> weight = learn((phi, vec_t), 1000)
>>> for p, t in zip(phi, vec_t):
...     print_result(p, weight, t)
p=0.58 +:+ OK
p=0.48 -:- OK
p=0.48 -:- OK
p=0.60 +:+ OK

>>> phi = array([
...     [ 1, 1, 0, 0],
...     [ 1,-1, 1, 1],
...     [ 1,-1, 1,-1],
...     [-1, 0, 1, 1],
...     [-1, 0, 1,-1],
...     [-1, 0,-1, 0],
...     ])

>>> vec_t = array([
...     [ 1, 0, 0, 0, 0, 0],
...     [ 0, 1, 0, 1, 0, 0],
...     [ 0, 0, 1, 0, 1, 1]])

>>> weights = [learn((phi, vec_t[i]), 1000) for i in range(3)]
>>> for i in range(3):
...     print(i)
...     for p, t in zip(phi, vec_t[i]):
...         print_result(p, weights[i], t)
0
p=0.80 +:+ OK
p=0.31 -:- OK
p=0.31 -:- OK
p=0.24 -:- OK
p=0.24 -:- OK
p=0.50 +:- NG
1
p=0.43 -:- OK
p=0.82 +:+ OK
p=0.35 -:- OK
p=0.79 +:+ OK
p=0.31 -:- OK
p=0.46 -:- OK
2
p=0.30 -:- OK
p=0.21 -:- OK
p=0.68 +:+ OK
p=0.29 -:- OK
p=0.77 +:+ OK
p=0.67 +:+ OK
"""

from pylab import *

# use L2 regularization
# without regularization, it may fail to invert mat_H.
WITH_REGULARIZATION = True

def sigmoid(x):
    return 1 / (1 + exp(-x))


def learn(data=None, num_iter=100):
    if not data:
        phi, vec_t = data_from_file()
    else:
        phi, vec_t = data

    NUM_DATA, NUM_FEATURES = phi.shape
    _NUM_DATA, = vec_t.shape
    assert NUM_DATA == _NUM_DATA

    weight = np.zeros(NUM_FEATURES)
    for i in range(num_iter):
        vec_y = np.vectorize(sigmoid)(weight.dot(phi.transpose()))
        mat_R = np.diag([yn * (1 - yn) for yn in vec_y])
        lambd = 1.0
        if WITH_REGULARIZATION:
            mat_H = phi.transpose().dot(mat_R).dot(phi) + lambd * np.eye(NUM_FEATURES)
            grad = (vec_y - vec_t).dot(phi) + lambd * weight
        else:
            mat_H = phi.transpose().dot(mat_R).dot(phi)
            grad = (vec_y - vec_t).dot(phi)
        w_new = weight - np.linalg.inv(mat_H).dot(grad)
        weight = w_new
    return weight


def get_prob(vec_x, weight):
    return sigmoid(array(vec_x).dot(weight))


def get_multi_prob(vec_x, weights):
    probs = [exp(vec_x.dot(w)) for w in weights]
    sum_probs = sum(probs)
    return [p / sum_probs for p in probs]


def sort_weight(weight):
    return list(sorted(enumerate(weight), key=lambda x:-abs(x[1])))


def print_result(vec_x, weight, t):
    y = get_prob(vec_x, weight)
    print "p=%.2f %s:%s %s" % (
        y,
        '0+-'[cmp(y, 0.5)],
        '-+'[t],
        ['NG', 'OK'][cmp(y, 0.5) == cmp(t, 0.5)]
        )


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
