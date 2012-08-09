#!/usr/bin/env python
from solvers.ctmc import ctmc, create_matrix, vector_mult

class CTMCSolution():

    def __init__(self, ss):
        self._ss = ss
        self._res = None
        self._actset = None
        self._steady_state_vector = None
        self._solve()


    def _solve(self):
        (self._res, self._actset) = self._ss.derive()
        self._steady_state_vector = (ctmc(create_matrix(self._res)))

    def get_steady_state_vector(self):
        return self._steady_state_vector

    def get_actions_throughoutput(self):
        act_vectors = {}
        ret_list = []
        vect_len = len(self._steady_state_vector)
        for (action,state) in self._actset.keys():
            if action not in act_vectors:
                act_vectors[action] = [0] * vect_len
            act_vectors[action][state-1] = self._actset[ (action, state) ]
        for action in act_vectors.keys():
            ret_list.append( (action, vector_mult(self._steady_state_vector, act_vectors[action])))
        return ret_list




