Using libpepa library
=====================

Large part of pypepa is libpepa library which can be used to embed PEPA calculations in your Python
project. The main entry point to libpepa is PEPAModel class. 

PEPAModel object
----------------

PEPAModel object needs be provided with keyword arguments:

* ``name`` - it is an optional argument. If it is not given, it will be become the basename of the
  ``file``, otherwise it will default to ``model`` (if modelstring is given)
* ``file`` - a path to a file with a PEPA model definition
* ``modelstring`` - a string with a PEPA model defintion
* ``solver`` - either ``sparse`` or ``direct``, default is ``sparse``

Basic usage:

.. code-block:: python

   from pypepa import PEPAModel

   pargs = {"file": "tests/simple.pepa"}
   pm = PEPAModel(**pargs)
   pm.derive()
 


