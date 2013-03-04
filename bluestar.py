"""
impl. of "BLUE*: a Blue-Fringe Procedure for Learning DFA with Noisy Data" Marc Sebban et. al.
"""

class DFA(object):
    def __init__(self):
        self.num_state = 1
        self.next_map = {0: {}}
        self.ok_map = {}
        self.color_map = {0: 'red'}

    def get_next_state(self, state, char):
        """
        returns state_id or None
        """
        return self.next_map[state].get(char)

    def add_new_state(self, state, char):
        """
        returns new state_id
        """
        new_state = self.num_state
        self.num_state += 1
        self.next_map[new_state] = {}
        self.next_map[state][char] = new_state
        if state == 0:
            self.color_map[new_state] = 'blue'

        return new_state

    def __repr__(self):
        """
        DFA{0+: {a->1}, 1: {a->2, b->4}, 2: {b->3}, 3+: {}, 4+: {}}
        0+ means state 0 acceptable
        {a->1} means if state 0 recieve 'a', move to state 1
        """
        buf = []
        for k in sorted(self.next_map):
            next = self.next_map[k]
            next_str = ', '.join('%s->%s' % p for p in next.items())
            if self.ok_map.get(k): k = str(k) + '+'
            buf.append('%s: {%s}' % (k, next_str))
        return 'DFA{%s}' % ', '.join(buf)

    def set_ok(self, state, b=True):
        self.ok_map[state] = True

    def exist_blue(self):
        return any(v == 'blue' for v in self.color_map.values())

    def get_blue(self):
        return [k for k in self.color_map if self.color_map[k] == 'blue']

    def get_red(self):
        return [k for k in self.color_map if self.color_map[k] == 'red']

    def is_ok(self, s):
        cur = 0
        for c in s:
            next = self.next_map[cur].get(c)
            if next == None:
                return False
            cur = next
        return self.ok_map.get(cur, False)

    def merge(self, x, y):
        from copy import deepcopy
        ret = DFA()
        ret.num_state = self.num_state - 1
        next_map = deepcopy(self.next_map)
        for k in next_map:
            for m in next_map[k]:
                if next_map[k][m] == x:
                    next_map[k][m] = y
        next_map[y].update(next_map[x])
        del next_map[x]
        ret.next_map = next_map
        ret.ok_map = deepcopy(self.ok_map)
        ret.color_map = deepcopy(self.color_map)
        return ret

def count_miss(dfa, eplus, eminus):
    miss = 0
    for e in eplus:
        if not dfa.is_ok(e):
            miss += 1
    for e in eminus:
        if dfa.is_ok(e):
            miss += 1
    return miss

def are_mergeable(dfa, x, y, eplus, eminus):
    miss_before = count_miss(dfa, eplus, eminus)
    tmp = dfa.merge(x, y)
    miss_after = count_miss(tmp, eplus, eminus)
    return (miss_after <= miss_before)  # TODO: relax

def do_best_promotion():
    pass

def do_best_merging():
    pass


def make_colored_prefix_tree_acceptor(data):
    """
    >>> make_colored_prefix_tree_acceptor(['aab', 'ab', ''])
    DFA{0+: {a->1}, 1: {a->2, b->4}, 2: {b->3}, 3+: {}, 4+: {}}
    >>> make_colored_prefix_tree_acceptor('aa aaaa aaaaaa'.split())
    DFA{0: {a->1}, 1: {a->2}, 2+: {a->3}, 3: {a->4}, 4+: {a->5}, 5: {a->6}, 6+: {}}
    >>> dfa = _
    >>> dfa.is_ok('aaaa')
    True
    >>> dfa.is_ok('a')
    False
    >>> dfa.is_ok('ab')
    False
    """
    dfa = DFA()
    for d in data:
        cur = 0
        for c in d:
            next = dfa.get_next_state(cur, c)
            if next == None:
                next = dfa.add_new_state(cur, c)
            cur = next
        dfa.set_ok(cur)
    return dfa


def bluestar(e_plus, e_minus):
    #import pdb; pdb.set_trace()
    dfa = make_colored_prefix_tree_acceptor(e_plus)
    while dfa.exist_blue():
        p = []
        m = []
        for b in dfa.get_blue():
            no_merge_found = True
            for r in dfa.get_red():
                if are_mergeable(dfa, b, r, e_plus, e_minus):
                    no_merge_found = False
                    m.append((b, r))
            if no_merge_found:
                p.append(b)

        if p:
            dfa = do_best_promotion(dfa, p)
        else:
            dfa = do_best_merging(dfa, m)

    return dfa


def _test():
    import doctest
    doctest.testmod()
    bluestar('aa aaaa aaaaaa'.split(), 'a aaa aaaaa'.split())
_test()
