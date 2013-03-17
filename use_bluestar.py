import subprocess
import bluestar

class Target(object):  # bad impl.
    def __init__(self):
        self.opened = False
        self.closed = False

    def open(self):
        self.opened = True

    def write(self):
        if not self.opened:
            raise RuntimeError
        if self.closed:
            raise RuntimeError

    def close(self):
        if not self.opened:
            raise RuntimeError
        self.closed = True


class Target(object):  # good impl.
    def __init__(self):
        self.opened = False

    def open(self):
        if self.opened:
            raise RuntimeError
        self.opened = True

    def write(self):
        if not self.opened:
            raise RuntimeError

    def close(self):
        if not self.opened:
            raise RuntimeError
        self.opened = False


e_plus = ['o', 'oc', 'ow', 'owc', 'oww', 'owwc', 'owww', 'oco', 'owco']
e_minus = ['c', 'w', 'ocw', 'ocoo', 'owwwo']

dfa = bluestar.bluestar(e_plus, e_minus)

def write_dfa(dfa):
    vertexes = []
    edges = []
    for v in dfa.next_map:
        if dfa.ok_map.get(v):
            shape = 'doublecircle'
        else:
            shape = 'circle'
        vertexes.append({'id': v, 'shape': shape})
        for c in dfa.next_map[v]:
            edges.append({'v0': v, 'v1': dfa.next_map[v][c], 'label': c})

    fo = open('t.dot', 'w')
    fo.write('digraph sample {\n')
    for v in vertexes:
        fo.write('%(id)s [label="%(id)s", shape="%(shape)s"];\n' % v)

    for e in edges:
        fo.write('%(v0)s -> %(v1)s [xlabel="%(label)s", fontcolor=blue];\n' % e)

    fo.write('}\n')
    fo.close()
    subprocess.check_call('dot -Tpng t.dot -o t.png', shell=True)


write_dfa(dfa)

def is_dfa_ok(dfa, s):
    state = 0
    for c in s:
        state = dfa.next_map[state].get(c)
        if state == None: return False

    return dfa.ok_map.get(state, False)


def is_foo_ok(s):
    target = Target()
    try:
        for c in s:
            if c == 'o':
                target.open()
            elif c == 'c':
                target.close()
            elif c == 'w':
                target.write()
    except:
        return False
    return True


def find_mismatch(dfa):
    chars = 'ocw'
    cur = [[c] for c in chars]
    next = []
    count = 0
    while cur:
        for s in cur:
            if len(s) > 20:
                print count
                print 'no mismatch found in len <= 20'
                return
            #print s
            count += 1
            d = is_dfa_ok(dfa, s)
            f = is_foo_ok(s)
            if d != f:
                print '%d: for input %s: dfa said %s, but target said %s' % (
                    count, s, d, f)
                return s
            if d:
                for c in chars:
                    next.append(s + [c])
        cur = next

find_mismatch(dfa)
