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
...     y = sigmoid(p.dot(weight))
...     print(y, y > 0.5, t, ((y > 0.5) == (t == 1)))
0.589573447422 True 1 True
0.310135768302 False 0 True
0.723316565544 True 1 True
0.589573447422 True 0 False
0.310135768302 False 0 True
0.723316565544 True 1 True
0.589573447422 True 1 True
0.310135768302 False 0 True
0.723316565544 True 1 True
"""

from pylab import *

# use L2 regularization
# without regularization, it may fail to invert mat_H.
WITH_REGULARIZATION = True

def data_from_file():
    phi = []  # feature matrix
    mat_t = []
    for line in file('3value.csv'):
        x, t = line.split('\t')
        phi.append([1] + [float(v) / 2 - 0.5 for v in x.split(',')[:-1]])
        mat_t.append(map(int, t.split(',')))
    phi = array(phi)
    mat_t = array(mat_t)
    NUM_DATA, NUM_FEATURES = phi.shape
    NUM_DATA2, NUM_CLASS = mat_t.shape
    assert NUM_DATA2 == NUM_DATA

    if not 'find largest teacher class':
        for i in range(NUM_CLASS):
            print i,
            vec_t = mat_t[:,i]
            print vec_t[vec_t != 0].shape

    vec_t = mat_t[:,14]
    phi = phi[vec_t != 0]
    vec_t = vec_t[vec_t != 0] / 2 + 0.5
    return phi, vec_t

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


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
