#!/usr/bin/env python3
'''
NieMarkov: Niema's Python implementation of Markov chains
'''

# imports
from random import randint

# useful constants
ALLOWED_STATE_TYPES = {int, str}

# helper function to check state type and throw an error if not allowed
def check_state_type(state_label):
    if type(state_label) not in ALLOWED_STATE_TYPES:
        raise TypeError("Invalid state type (%s). Must be one of: %s" % (type(state_label), ', '.join(str(t) for t in ALLOWED_STATE_TYPES)))

# helper function to randomly pick from a `dict` of options (keys = options, values = count weighting that option)
def random_choice(options):
    sum_options = sum(options.values())
    random_int = randint(1, sum_options)
    curr_total_count = 0
    for option, count in options.items():
        curr_total_count += count
        if random_int <= curr_total_count:
            return option

# class to represent Markov chains
class MarkovChain:
    # initialize a `MarkovChain` object
    def __init__(self, order=1):
        if not isinstance(order, int) or order < 1:
            raise ValueError("`order` must be a positive integer")
        self.order = order                # order of this Markov chain
        self.labels = list()              # labels of the states of this Markov chain
        self.label_to_state = dict()      # `label_to_state[label]` is the state (`int` from 0 to `num_states-1`) labeled by `label`
        self.transitions = dict()         # for an `order`-dimensional `tuple` of states `state_tuple`, `transitions[state_tuple]` is a `dict` where keys = outgoing state tuples, and values = transition counts
        self.initial_state_tuple = dict() # `initial_state_tuple[state_tuple]` is the number of times `state_tuple` is at the start of a path

    # add a path to this `MarkovChain`
    def add_path(self, path):
        # check `path` for validity
        if not isinstance(path, list):
            raise TypeError("`path` must be a list of state labels")
        if len(path) <= self.order:
            raise ValueError("Length of `path` (%d) must be > Markov chain order (%d)" % (len(path), self.order))


        # add new state labels
        for state_label in path:
            if state_label not in self.label_to_state:
                check_state_type(state_label)
                self.label_to_state[state_label] = len(self.labels)
                self.labels.append(state_label)

        # add path
        first_tup = tuple(self.label_to_state[path[j]] for j in range(self.order))
        if first_tup in self.initial_state_tuple:
            self.initial_state_tuple[first_tup] += 1
        else:
            self.initial_state_tuple[first_tup] = 1
        for i in range(len(path) - self.order):
            from_tup = tuple(self.label_to_state[path[j]] for j in range(i, i+self.order))
            to_tup = tuple(self.label_to_state[path[j]] for j in range(i+1, i+1+self.order))
            if from_tup in self.transitions:
                if to_tup in self.transitions[from_tup]:
                    self.transitions[from_tup][to_tup] += 1
                else:
                    self.transitions[from_tup][to_tup] = 1
            else:
                self.transitions[from_tup] = {to_tup: 1}

    # generate a random path in this `MarkovChain`
    def generate_path(self, max_len=float('inf')):
        curr_state_tuple = random_choice(self.initial_state_tuple)
        path = [self.labels[state] for state in curr_state_tuple]
        while len(path) < max_len:
            if curr_state_tuple not in self.transitions:
                break
            curr_state_tuple = random_choice(self.transitions[curr_state_tuple])
            path.append(self.labels[curr_state_tuple[-1]])
        return path
