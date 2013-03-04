"""
impl. of "BLUE*: a Blue-Fringe Procedure for Learning DFA with Noisy Data" Marc Sebban et. al.
"""

class DFA(object):
    def __init__(self):
        self.num_state = 1
        self.next_map = {0: {}}
        self.ok_map = {}

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
        pass

    def get_blue(self):
        pass


def make_colored_prefix_tree_acceptor(data):
    """
    >>> make_colored_prefix_tree_acceptor(['aab', 'ab', ''])
    DFA{0+: {a->1}, 1: {a->2, b->4}, 2: {b->3}, 3+: {}, 4+: {}}
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
    dfa = make_colored_prefix_tree_acceptor(e_plus)
    while dfa.exist_blue():
        p = []
        m = []
        for b in dfa.get_blue():
            no_merge_found = True
            for r in dfa.get_red():
                if are_mergeable(dfa, b, r):
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

_test()
