#!/usr/bin/env python
# coding: utf-8

from matplotlib import pyplot as plt
import argparse


def parse_line(line):
    return list(map(float, line.strip().split()))

def process_lines(lines):
    results = dict()
    assert(lines[0].startswith('dataset No.'))
    for i, measure in enumerate(('RD', 'RR', 'RC')):
        results[measure] = {'psl': dict(), 'fairpsl':dict()}
        start = 3 + 7 * i 
        assert(lines[start] == '----------%s---------------'%measure)
        results[measure]['psl']['score'] = parse_line(lines[start+2])[0]
        results[measure]['psl']['accuracy'] = parse_line(lines[start+3])[0]
        results[measure]['fairpsl']['score'] = parse_line(lines[start+5])
        results[measure]['fairpsl']['accuracy'] = parse_line(lines[start+6])
    return results


def extract_results(input_file):
    with open(input_file) as f:
        input_str = f.read()
    lines = input_str.splitlines()
    start_indices = []
    for i, line in enumerate(lines):
        if line.startswith('dataset No.'):
            start_indices.append(i)

    results = []
    for i in start_indices:
        results.append(process_lines(lines[i:i+26]))
    return results


def plot_results(results, pdf_filename):
    num_datasets = len(results)
    cmap = plt.get_cmap('tab10')

    plt.figure(figsize=(15, 3))
    for i, measure in enumerate(('RD', 'RR', 'RC')):
        plt.subplot(1, 3, i+1)
        x = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
        y_psl = []
        y_fpsl = []
        for result in results:
            y_psl.append([result[measure]['psl']['score'] for _ in range(6)])
            y_fpsl.append(list(result[measure]['fairpsl']['score']))

        lines = []
        labels = []
        for j in range(num_datasets):
            color = cmap(j)
            y = y_fpsl[j]
            line = plt.plot(x, y, 'o-', color=color)
            lines.append(line[0])
            labels.append('FairPSL(%d)'%(j+1))

            y = y_psl[j]
            line = plt.plot(x, y, '--', color=color)
            lines.append(line[0])
            labels.append('PSL(%d)'%(j+1))

        plt.xlim([0.001, 0.5])
        plt.xscale('log')
        _ = plt.xticks(x, x)
        _ = plt.xlabel(r'$\delta$', fontsize=15)
        _ = plt.ylabel(measure, fontsize=15)

    _ = plt.figlegend(lines, labels, loc ='upper center', ncol=len(results), columnspacing=7, 
                      borderaxespad=0)
    plt.subplots_adjust(top=0.8)
    plt.savefig(pdf_filename, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('result_file', help='the output of experiments')
    parser.add_argument('pdf_file', help='the pdf file for rendering the plots')
    args = parser.parse_args()

    results = extract_results(args.result_file)
    plot_results(results, args.pdf_file)
