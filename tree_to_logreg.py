# -*- coding: utf-8 -*-
"""
tree to logistic regression
"""
from pylab import *
import logreg

def print_mat(x):
    for line in x:
        print ' '.join('% 0.2f' % p for p in line)

# one way tree
# if q_i == +1 then a_i == +1
def one_way_tree():
    SIZE = 4
    NUM_QUESTION = SIZE - 1
    NUM_ANSWER = SIZE
    NUM_DATA = SIZE
    mat_phi = np.zeros((NUM_DATA, NUM_QUESTION))
    mat_t = np.zeros((NUM_DATA, NUM_ANSWER))
    for i in range(NUM_DATA):
        mat_t[i][i] = 1.0
        for j in range(i):
            mat_phi[i, j] = -1.0
        if i < NUM_QUESTION:
            mat_phi[i, i] = +1.0

    weights = [logreg.learn((mat_phi, mat_t[:, i])) for i in range(NUM_ANSWER)]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    print_mat(np.array(weights))

# graph to data
# graph :: [(qid, yes link, no link)]
# link :: vertex_id when positive, answer_id when negative
graph = [
    [0, ~0, 1],
    [1, ~1, 2],
    [2, ~2, ~3]
]

def graph2data(graph, start=0, NUM_QUESTION=None, NUM_ANSWER=None):
    """
    >>> for d in graph2data(graph, 0, 3, 4): print d
    (array([ 1.,  0.,  0.]), array([ 1.,  0.,  0.,  0.]))
    (array([-1.,  1.,  0.]), array([ 0.,  1.,  0.,  0.]))
    (array([-1., -1.,  1.]), array([ 0.,  0.,  1.,  0.]))
    (array([-1., -1., -1.]), array([ 0.,  0.,  0.,  1.]))
    """
    if not NUM_QUESTION:
        NUM_QUESTION = len(set(g[0] for g in graph))
    if not NUM_ANSWER:
        NUM_ANSWER = len(set(~g[i] for g in graph for i in [1, 2] if g[i] < 0))

    if start < 0:  # link to answer
        answer = np.zeros(NUM_ANSWER)
        answer[~start] = 1.0
        return [(np.zeros(NUM_QUESTION), answer)]
    qid, yes, no = graph[start]
    ret = []
    for q, a in graph2data(graph, yes, NUM_QUESTION, NUM_ANSWER):
        q[qid] = +1.0
        ret.append((q, a))
    for q, a in graph2data(graph, no, NUM_QUESTION, NUM_ANSWER):
        q[qid] = -1.0
        ret.append((q, a))
    return ret


def square():
    graph = [
        [0,  1,  2],
        [1, ~0,  3],
        [2, ~1,  3],
        [3, ~1, ~0],
    ]
    NUM_QUESTION = len(set(g[0] for g in graph))
    assert NUM_QUESTION == 4
    NUM_ANSWER = len(set(~g[i] for g in graph for i in [1, 2] if g[i] < 0))
    assert NUM_ANSWER == 2

    data = graph2data(graph, 0, NUM_QUESTION, NUM_ANSWER)
    NUM_DATA = len(data)
    mat_phi = np.array([d[0] for d in data])
    mat_t = np.array([d[1] for d in data])

    weights = [logreg.learn((mat_phi, mat_t[:, i])) for i in range(NUM_ANSWER)]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    print weights


def graph2all_data(graph, start=0, NUM_QUESTION=None, NUM_ANSWER=None, add_offset_column=False):
    if not NUM_QUESTION:
        NUM_QUESTION = len(set(g[0] for g in graph))
    if not NUM_ANSWER:
        NUM_ANSWER = len(set(~g[i] for g in graph for i in [1, 2] if g[i] < 0))
    def find_answer(q):
        cur = start
        while True:
            if cur < 0:
                answer = np.zeros(NUM_ANSWER)
                answer[~cur] = 1.0
                return answer
            qid, yes, no = graph[cur]
            if q[qid] == 1:
                cur = yes
            else:
                cur = no

    from itertools import product
    qs = product([-1, 1], repeat=NUM_QUESTION)
    for q in qs:
        if add_offset_column:
            q = list(q) + [1]
        yield (q, find_answer(q))


def with_all_data(graph=graph):
    "with all data"
    data = list(graph2all_data(graph))
    mat_phi = np.array([d[0] for d in data])
    print mat_phi
    mat_t = np.array([d[1] for d in data])
    print mat_t

    weights = [logreg.learn((mat_phi, mat_t[:, i])) for i in range(mat_t.shape[1])]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    print_mat(weights)
    return weights

def with_all_data_large(SIZE=10):
    # 5 -> 1sec
    # 7 -> 3sec
    # 10 -> 30sec
    graph = [
        [i, ~i, i + 1]
        for i in range(SIZE)
    ]
    graph[-1][-1] = ~SIZE
    with_all_data(graph)


def one_way_tree2():
    SIZE = 10
    NUM_QUESTION = SIZE - 1
    NUM_ANSWER = SIZE
    NUM_DATA = SIZE
    mat_phi = np.zeros((NUM_DATA, NUM_QUESTION))
    mat_t = np.zeros((NUM_DATA, NUM_ANSWER))
    for i in range(NUM_DATA):
        mat_t[i][i] = 1.0
        for j in range(i):
            mat_phi[i, j] = -1.0
        if i < NUM_QUESTION:
            mat_phi[i, i] = +1.0

    weights = [logreg.learn((mat_phi, mat_t[:, i])) for i in range(NUM_ANSWER)]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    from itertools import product
    qs = product([-1, 1], repeat=NUM_QUESTION)
    num_ok = 0
    for q in qs:
        if not 1.0 in q:
            a = NUM_ANSWER - 1
        #else:
        #    a = q.index(1.0)
        probs = logreg.get_multi_prob(np.array(q), weights)
        if np.array(probs).argmax() == a:
            num_ok += 1
    print num_ok / (2.0 ** NUM_QUESTION)


def correct_ratio(NUM_QUESTION, NUM_ANSWER, weights, add_offset_column=False):
    from itertools import product
    qs = product([-1, 1], repeat=NUM_QUESTION)
    num_ok = 0
    for q in qs:
        if not 1.0 in q:
            a = NUM_ANSWER - 1
        else:
            a = q.index(1.0)
        if add_offset_column:
            q = list(q) + [1]
        probs = logreg.get_multi_prob(np.array(q), weights)
        if np.array(probs).argmax() == a:
            num_ok += 1
        else:
            print ''.join(' +-'[x] for x in q), a, np.array(probs).argmax()

    return num_ok / (2.0 ** NUM_QUESTION)


def with_all_data_large_2():
    # 5 -> 1sec
    # 7 -> 3sec
    # 10 -> 30sec
    SIZE = 10
    NUM_QUESTION = SIZE + 1
    NUM_ANSWER = SIZE + 1
    graph = [
        [i, ~i, i + 1]
        for i in range(SIZE)
    ]
    graph[-1][-1] = ~SIZE
    weights = with_all_data(graph)
    print correct_ratio(NUM_QUESTION - 1, NUM_ANSWER, weights)


def generate_tree_graph(SIZE):
    graph = [
        [i, ~i, i + 1]
        for i in range(SIZE)
    ]
    graph[-1][-1] = ~SIZE
    return graph


def sampling():
    "sampling from all data"
    SIZE = 10
    NUM_QUESTION = SIZE
    NUM_ANSWER = SIZE + 1
    graph = generate_tree_graph(SIZE)
    data = list(graph2all_data(graph))
    from random import shuffle
    shuffle(data)
    data = data[:11]
    mat_phi = np.array([d[0] for d in data])
    print mat_phi
    mat_t = np.array([d[1] for d in data])
    print mat_t

    weights = [logreg.learn((mat_phi, mat_t[:, i])) for i in range(mat_t.shape[1])]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    print_mat(weights)
    print correct_ratio(NUM_QUESTION, NUM_ANSWER, weights)
    return weights


def change_scale(size=10, add_offset_column=True):
    SIZE = 10
    NUM_QUESTION = SIZE
    NUM_ANSWER = SIZE + 1
    graph = [
        [i, ~i, i + 1]
        for i in range(SIZE)
    ]
    graph[-1][-1] = ~SIZE
    data = list(graph2all_data(graph, add_offset_column=add_offset_column))
    mat_phi = np.array([d[0] for d in data])
    mat_phi[:,1] *= 10
    mat_phi[:,3] *= 100
    print mat_phi
    mat_t = np.array([d[1] for d in data])
    print mat_t

    weights = [logreg.learn((mat_phi, mat_t[:, i]), 1000) for i in range(mat_t.shape[1])]

    for d in mat_phi:
        probs = logreg.get_multi_prob(d, weights)
        print d
        print ' '.join('%0.2f' % p for p in probs)

    print_mat(weights)
    print correct_ratio(NUM_QUESTION, NUM_ANSWER, weights, add_offset_column=add_offset_column)

#change_scale(10, False)
change_scale(10, True)

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main_':
    _test()
