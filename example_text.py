#!/usr/bin/env python3
'''
Example script that uses NieMarkov to build a Markov model from a text file and generate a sentence
'''
from niemarkov import MarkovChain
from sys import argv
if __name__ == "__main__":
    # load data
    assert len(argv) == 3, "USAGE: %s <text_file> <order>"
    order = int(argv[2])
    with open(argv[1], 'rt') as f:
        raw_text = f.read()
    for symbol in ['“', '”', '"']:
        raw_text = raw_text.replace(symbol, '')
    words = [s.strip() for s in raw_text.strip().split()]

    # build Markov Chain and generate a sentence
    mc = MarkovChain(order=order)
    path = list()
    for word in words:
        path.append(word)
        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
            if len(path) > order:
                mc.add_path(path)
            path = list()
    print(' '.join(mc.generate_path()))
