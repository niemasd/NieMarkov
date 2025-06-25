#!/usr/bin/env python3
'''
Example script that uses NieMarkov to build a Markov model from a text file and generate a sentence
'''
from niemarkov import MarkovChain
from sys import argv
if __name__ == "__main__":
    # parse user args
    assert len(argv) in {2,3} and argv[1].replace('-', '').strip().lower() not in {'h', 'help'}, "USAGE: %s <txt/model> [order=1]"
    if len(argv) == 3:
        order = int(argv[2])
    else:
        order = 1
    fn_lower = argv[1].strip().lower()

    # load a NieMarkov model if given a model file
    try:
        mc = MarkovChain.load(argv[1])

    # build a NieMarkov model from a text file
    except:
        # load and clean text
        with open(argv[1], 'rt') as f:
            raw_text = f.read()
        for symbol in ['“', '”', '"']:
            raw_text = raw_text.replace(symbol, '')
        words = [s.strip() for s in raw_text.strip().split()]

        # build NieMarkov model and dump it to a JSON
        mc = MarkovChain(order=order)
        path = list()
        for word in words:
            path.append(word)
            if word.endswith('.') or word.endswith('!') or word.endswith('?'):
                if len(path) > order:
                    mc.add_path(path)
                path = list()
        mc.dump(argv[1] + '.pkl.gz')

    # print summary info about the model, and generate a string of text
    print(mc)
    print(' '.join(mc.generate_path()))
