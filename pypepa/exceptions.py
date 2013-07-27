# -*- coding: utf-8 -*-

class PyPEPAException(RuntimeError):
    """ General exception """

class VariableAlreadyDefinedError(PyPEPAException):
    """ already defined """

class ProcessAlreadyDefinedError(PyPEPAException):
    """ Process already defined """

class VariableNotDefinedError(PyPEPAException):
    """ Var has not been defined """

class ProcessNotDefinedError(PyPEPAException):
    """ Process not defined """

class DeadlockError(PyPEPAException):
    """ Deadlock found """

class InvalidActionTypeError(PyPEPAException):
    """ Tau in syncset """

