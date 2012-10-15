#!/usr/bin/env python
from solvers.ctmc import ctmc, ctmc_sparse, create_matrix, vector_mult, create_lil_matrix, ctmc_transient
from pprint import pprint
class CTMCSolution():

    def __init__(self, ss, solver):
        self._ss = ss
        self._res = None
        self._actset = None
        self._solver = solver
        self._steady_state_vector = None


    def solve_transient(self,stop, start):
        (self._res, self._actset) = self._ss.derive()
        matrix = create_matrix(self._res)
        a = ctmc_transient(matrix, len(self._res),0, stop)
        print(a)

    def solve_steady(self):
        (self._res, self._actset) = self._ss.derive()
        if self._solver == "direct":
            self._steady_state_vector = (ctmc(create_matrix(self._res)))
        elif self._solver == "sparse":
            pprint(self._res)
            self._steady_state_vector = (ctmc_sparse(create_lil_matrix(self._res), len(self._res)))

    def get_steady_state_vector(self):
        return self._steady_state_vector

    def get_actions_throughoutput_from_vector(self, v):
        """ Calculates throughoutput of vector """
        act_vectors = {}
        ret_list = []
        vect_len = len(v)
        for (action,state) in self._actset.keys():
            if action not in act_vectors:
                act_vectors[action] = [0] * vect_len
            act_vectors[action][state-1] = self._actset[ (action, state) ]
        for action in act_vectors.keys():
            ret_list.append( (action, vector_mult(v, act_vectors[action])))
        return ret_list

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




