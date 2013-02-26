# -*- coding: utf-8 -*-
"""
CART

>>> tree = Node(parse_data(test_data))
>>> tree
<[++A, +-B, --C]>
>>> grow(tree)
<f=0, yes=<[++A, +-B]>, no=<[--C]>>
>>> grow(tree)
<f=0, yes=<f=1, yes=<[++A]>, no=<[+-B]>>, no=<[--C]>>
"""
from collections import Counter, namedtuple
from random import choice

test_data = '''
++A
+-B
--C
'''

class Data(object):
    def __init__(self, x, t):
        self.x = x
        self.t = t

    def __repr__(self):
        return self.x + self.t


class Node(object):
    def __init__(self, data=[], feature=None, yes=None, no=None):
        self.data = data
        self.feature = feature
        self.yes = yes
        self.no = no

    def __repr__(self):
        if self.feature == None:
            return '<%r>' % self.data
        return '<f=%d, yes=%r, no=%r>' % (self.feature, self.yes, self.no)


def gini(*args):
    """
    >>> gini(1, 1)
    1.0
    >>> gini(2, 0)
    0.0
    >>> gini(2, 1)
    1.3333333333333333
    >>> gini(*Counter("AAB").values())
    1.3333333333333333
    """
    s = sum(args)
    if s == 0: return 0.0
    return (1 - float(sum(x * x for x in args)) / s / s) * s


def calc_total_gini(leaf):
    ret = 0
    for l in leaf:
        ret += gini(*Counter(d.x for d in l.data).values())
    return ret


def grow(node):
    # find all leaf
    leaf = []
    to_visit = [node]
    while to_visit:
        n = to_visit.pop()
        if n.data:
            leaf.append(n)
        else:
            to_visit.append(n.yes)
            to_visit.append(n.no)

    NUM_FEATURES = len(leaf[0].data[0].x)

    total_gini = calc_total_gini(leaf)
    best_score = 0
    best_split = None
    yes = Node([], None, None, None)
    no = Node([], None, None, None)
    for l in leaf:
        before = calc_total_gini([l])
        for i in range(NUM_FEATURES):
            yes.data = [d for d in l.data if d.x[i] == '+']
            no.data = [d for d in l.data if d.x[i] == '-']
            after = calc_total_gini([yes, no])
            if before - after > best_score:
                best_score = before - after
                best_split = (l, i)

    if not best_split:
        return None

    l, i = best_split
    yes.data = [d for d in l.data if d.x[i] == '+']
    no.data = [d for d in l.data if d.x[i] == '-']
    l.data = []
    l.feature = i
    l.yes = yes
    l.no = no

    return node


def parse_data(s):
    """
    >>> parse_data(test_data)
    [++A, +-B, --C]
    """
    s = s.strip().split('\n')
    data = []
    CLASS = []
    NUM_FEATURES = None
    for line in s:
        t = line[-1]
        x = line[:-1]
        if t not in CLASS:
            CLASS.append(t)
        if not NUM_FEATURES:
            NUM_FEATURES = len(x)
        else:
            assert len(x) == NUM_FEATURES
        data.append(Data(x, t))
    return data


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
