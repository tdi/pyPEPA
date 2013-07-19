import unittest

from pypepa import PEPAModel
from pypepa.exceptions import VariableNotDefinedError, VariableAlreadyDefinedError, \
                              ProcessAlreadyDefinedError, ProcessNotDefinedError
from pprint import pprint

GENDOTS_DIR = "test_dots_x789/"

class PyPEPATestCase(unittest.TestCase):

    def compare_up_to(self, value, value2, ratio):
        """ Returns true if value ~ value2+-ratio% """
        return value2-value2*ratio <= value <= value2+value2*ratio

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_steady(self):
        pargs = {"file": "tests/simple.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.steady_state()
        ss = pm.get_steady_state_vector()
        assert len(ss) == 4
        assert self.compare_up_to(float(ss[0]), 0.33333333, 0.1)
        assert self.compare_up_to(float(ss[1]), 0.33333333, 0.1)
        assert self.compare_up_to(float(ss[2]), 0.16666666, 0.1)
        assert self.compare_up_to(float(ss[3]), 0.16666666, 0.1)

    def test_perf(self):
        pargs = {"file": "tests/simple.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.steady_state()
        ss = pm.get_throughoutput()
        assert self.compare_up_to(float(ss[0][1]), 1.166666666, 0.1)
        assert self.compare_up_to(float(ss[1][1]), 1.166666666, 0.1)

    def test_gendots(self):
        import os
        os.makedirs(GENDOTS_DIR)
        pargs = {"file": "tests/simple.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.generate_dots(GENDOTS_DIR)
        assert os.path.isdir(GENDOTS_DIR)
        assert os.path.exists(GENDOTS_DIR + "P.dot")
        assert os.path.exists(GENDOTS_DIR + "Q.dot")
        assert os.path.exists(GENDOTS_DIR + "simple.pepa.dot")
        os.remove(GENDOTS_DIR + "P.dot")
        os.remove(GENDOTS_DIR + "Q.dot")
        os.remove(GENDOTS_DIR + "simple.pepa.dot")
        os.removedirs(GENDOTS_DIR)

    def test_steady_expressions(self):
        pargs = {"file": "tests/simple_expr.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.steady_state()
        ss = pm.get_steady_state_vector()
        assert len(ss) == 4
        assert self.compare_up_to(float(ss[0]), 0.33333333, 0.1)
        assert self.compare_up_to(float(ss[1]), 0.33333333, 0.1)
        assert self.compare_up_to(float(ss[2]), 0.16666666, 0.1)
        assert self.compare_up_to(float(ss[3]), 0.16666666, 0.1)

    def test_utilisation(self):
        pargs = {"file": "tests/simple.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.steady_state()
        uts = pm.get_utilisations()
        assert uts[0]["P1"]==0.5
        assert self.compare_up_to(float(uts[0]['P']), 0.499999, 0.1)
        assert self.compare_up_to(float(uts[1]['Q']), 0.666666666, 0.1)
        assert self.compare_up_to(float(uts[1]['Q1']), 0.33333333333, 0.1)

    def test_perf_expressions(self):
        pargs = {"file": "tests/simple_expr.pepa", "solver" : "direct"}
        pm = PEPAModel(**pargs)
        pm.derive()
        pm.steady_state()
        ss = pm.get_throughoutput()
        assert self.compare_up_to(float(ss[0][1]), 1.166666666, 0.1)
        assert self.compare_up_to(float(ss[1][1]), 1.166666666, 0.1)

    def test_rate_not_defined(self):
        pargs = {"file": "tests/bad_rate.pepa", "solver" : "direct"}
        self.assertRaises(VariableNotDefinedError, PEPAModel, **pargs)

    def test_rate_already_defined(self):
        pargs = {"file": "tests/already_rate.pepa", "solver" : "direct"}
        self.assertRaises(VariableAlreadyDefinedError, PEPAModel, **pargs)
 
    def test_process_not_defined(self):
        pargs = {"file": "tests/bad_process.pepa", "solver" : "direct"}
        self.assertRaises(ProcessNotDefinedError, PEPAModel, **pargs)

    def test_process_already_defined(self):
        pargs = {"file": "tests/already_process.pepa", "solver" : "direct"}
        self.assertRaises(ProcessAlreadyDefinedError, PEPAModel, **pargs)
    
        


