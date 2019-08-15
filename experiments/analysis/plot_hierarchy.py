#!/usr/bin/env python
# coding: utf-8

import tempfile, os, subprocess, argparse

def read_hierarchy(label_file, manager_file):

    labels = dict()
    with open(label_file) as f:
        for line in f:
            line = line.split()
            labels[line[0]] = line[1]

    managers = dict()
    with open(manager_file) as f:
        for line in f:
            m, e = line.split()
            managers.setdefault(e, []).append(m)
            
    managers = {k: frozenset(v) for k, v in managers.items()}

    top_manager = list(set(labels.keys()) - set(managers.keys()))[0]
    managers[top_manager] = frozenset([])

    parents = dict()
    for e, m_set in managers.items():
        parents.setdefault(m_set, []).append(e)

    hierarcy_tree = []
    Q = [top_manager]
    while Q:
        m = Q.pop()
        e_managers = frozenset(managers[m] | set([m]))
        if not e_managers in parents:
            continue
        for e in parents[e_managers]:
            hierarcy_tree.append((m, e))
            Q.append(e)

    return hierarcy_tree, labels



def get_dotstr(hierarcy_tree, labels):
    possible_labels = list(set(labels.values()))
    dotstr = 'digraph heirarchy {\n\n'
    for e in labels:
        style_str = ''
        if labels[e] == possible_labels[0]:
            style_str = ', style=filled'
        dotstr += ' node_%s [label="%s", shape=circle%s];\n'%(e, e, style_str)
    for m, e in hierarcy_tree:
        dotstr += ' node_%s -> node_%s ;\n'%(m, e)

    dotstr += '\n}'
    return dotstr




def create_pdf(label_file, manager_file, pdf_file):
    hierarcy_tree, labels = read_hierarchy(label_file, manager_file)
    dotstr = get_dotstr(hierarcy_tree, labels)
    fd, fname = tempfile.mkstemp(suffix='.dot')
    with open(fname, 'w') as f:
        print(dotstr, file=f)

    cmd = ['dot', '-Tpdf', fname, '-o', pdf_file]
    subprocess.check_call(cmd)

    os.close(fd)
    os.remove(fname)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label_file', help='the file containing labels of employee')
    parser.add_argument('manager_file', help='the file containing the manager relationships')
    parser.add_argument('pdf_file', help='the output pdf file')
    args = parser.parse_args()

    create_pdf(args.label_file, args.manager_file, args.pdf_file)
