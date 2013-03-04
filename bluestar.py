"""
impl. of "BLUE*: a Blue-Fringe Procedure for Learning DFA with Noisy Data" Marc Sebban et. al.



"""
from math import sqrt
from scipy import stats
risk = 0.5  # alpha in the paper: risk factor: 0.5<- strongest .. weakest->0
ualpha = stats.norm().ppf(1 - risk)  # ppf: percentile point function

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
            suffix = ''
            color = self.color_map.get(k)
            if color == 'red':
                suffix += 'r'
            elif color == 'blue':
                suffix += 'b'
            elif color == 'none': # color removed
                pass
            else:
                suffix += 'w'

            if self.ok_map.get(k): suffix += '+'
            buf.append('%s%s: {%s}' % (k, suffix, next_str))
        return 'DFA{%s}' % ', '.join(buf)

    def set_ok(self, state, b=True):
        self.ok_map[state] = True

    def exist_blue(self):
        return any(v == 'blue' for v in self.color_map.values())

    def get_blue(self):
        return [k for k in self.next_map if self.color_map.get(k) == 'blue']

    def get_red(self):
        return [k for k in self.next_map if self.color_map.get(k) == 'red']

    def is_ok(self, s):
        cur = 0
        for c in s:
            next = self.next_map[cur].get(c)
            if next == None:
                return False
            cur = next
        return self.ok_map.get(cur, False)

    def is_blue(self, k):
        return self.color_map[k] == 'blue'

    def is_red(self, k):
        return self.color_map[k] == 'red'

    def merge(self, x, y):
        from copy import deepcopy
        assert self.is_blue(x)
        assert self.is_red(y)
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
        del ret.color_map[x]
        assert ret.color_map[y] == 'red'
        for s in next_map[y].values():
            if ret.color_map.get(s) != 'red':
                ret.color_map[s] = 'blue'
        return ret

    def remove_unreachable(self):
        earned = 0
        reachable = []
        todo = [0]
        while todo:
            cur = todo.pop()
            reachable.append(cur)
            for next in self.next_map[cur].values():
                if next not in reachable and next not in todo:
                    todo.append(next)

        for k in self.next_map.keys():
            if k not in reachable:
                del self.next_map[k]
                if self.color_map.has_key(k):
                    del self.color_map[k]
                earned += 1

        return earned

    def remove_color(self):
        for k in self.color_map:
            self.color_map[k] = 'none'

def count_miss(dfa, e_plus, e_minus):
    miss = 0
    for e in e_plus:
        if not dfa.is_ok(e):
            miss += 1
    for e in e_minus:
        if dfa.is_ok(e):
            miss += 1
    return miss



def _tmp_merge(dfa, x, y, e_plus, e_minus):
    miss_before = count_miss(dfa, e_plus, e_minus)
    tmp = dfa.merge(x, y)
    miss_after = count_miss(tmp, e_plus, e_minus)
    N = float(len(e_plus) + len(e_minus))
    return miss_before, miss_after, N, tmp


def are_mergeable(dfa, x, y, e_plus, e_minus):
    print 'are_mergeable %s and %s?' % (x, y)
    miss_before, miss_after, N, _ = _tmp_merge(dfa, x, y, e_plus, e_minus)
    print 'miss %d->%d' % (miss_before, miss_after)
    print 'miss not inclease?', (miss_after <= miss_before)
    #return (miss_after <= miss_before)
    #import pdb; pdb.set_trace()
    phat = (miss_before + miss_after) / N / 2

    zalpha = ualpha * sqrt(2 * phat * (1 - phat) / N)
    T = (miss_after - miss_before) / N
    print 'p^=%s, zalpha=%s, T=%s, margeable?=%s' % (phat, zalpha, T, T <= zalpha)
    if T <= zalpha:
        return True
    return False


def do_best_promotion(dfa, promotable, e_plus, e_minus):
    buf2 = []
    for b in promotable:
        buf = []
        for r in dfa.get_red():
            miss_before, miss_after, N, _ = _tmp_merge(dfa, b, r, e_plus, e_minus)
            phat = (miss_before + miss_after) / N / 2
            z = (miss_after / N - miss_before / N) / sqrt(2 * phat * (1 - phat) / N)
            buf.append(z)
        buf2.append((max(buf), b))
    buf2.sort()
    best = buf2[0][1]

    dfa.color_map[best] = 'red'
    for s in dfa.next_map[best].values():
        if dfa.color_map.get(s) != 'red':
            dfa.color_map[s] = 'blue'

    return dfa


def do_best_merging(dfa, mergable, e_plus, e_minus):
    print 'merge', mergable
    print dfa
    delta = 1.0
    buf = []
    for b, r in mergable:
        miss_before, miss_after, N, tmp = _tmp_merge(dfa, b, r, e_plus, e_minus)
        n = tmp.remove_unreachable() + 1
        phat = (miss_before + miss_after) / N / 2
        zalpha = ualpha * sqrt(2 * phat * (1 - phat) / N)
        denom = sqrt(2 * phat * (1 - phat) / N)
        if denom != 0.0:
            beta = stats.norm().cdf(zalpha - delta / denom)
        else:
            beta = 1.0
        buf.append((beta / n, tmp, (b, r)))

    buf.sort()
    ret = buf[0][1]
    print 'best merge:', buf[0][2]
    print '->', ret
    return ret


def make_colored_prefix_tree_acceptor(data):
    """
    >>> make_colored_prefix_tree_acceptor('aa aaaa aaaaaa'.split())
    DFA{0r: {a->1}, 1b: {a->2}, 2w+: {a->3}, 3w: {a->4}, 4w+: {a->5}, 5w: {a->6}, 6w+: {}}
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
            print 'promote'
            print dfa
            dfa = do_best_promotion(dfa, p, e_plus, e_minus)
            print '->', dfa
        else:
            assert m
            dfa = do_best_merging(dfa, m, e_plus, e_minus)
        print dfa.exist_blue()
    dfa.remove_unreachable()
    dfa.remove_color()
    return dfa


def _test():
    import doctest
    doctest.testmod()
    #bluestar('aa aaaa aaaaaa'.split(), 'a aaa aaaaa'.split())
    #print bluestar('ba baa aaa aaaa baaa aaaaaa aaaaaaaaaaa'.split(), 'bb bbb aab abab aaaba'.split())
    #print bluestar('a', 'b')
    #print bluestar('a b'.split(), 'c')
    #print bluestar('aa ba'.split(), '')
    #print bluestar('aa ba'.split(), 'b')
    #print bluestar('aa aba abba abbba abbbba abbbbba'.split(), 'b ab abab aaa'.split())
    print bluestar('ab aab abb aabb'.split(), 'a b'.split())
_test()
