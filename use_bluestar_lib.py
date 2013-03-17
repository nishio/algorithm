import subprocess

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


