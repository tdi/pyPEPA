Using libpepa library
=====================

Large part of pypepa is libpepa library which can be used to embed PEPA calculations in your Python
project. The main entry point to libpepa is PEPAModel class. 

PEPAModel object
----------------

PEPAModel object needs be provided with keyword arguments:

.. autoclass:: pypepa.PEPAModel

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
 
After that the PEPA model is derived. Now, in order to make some calculations you need to 
use corresponding methods from ``PEPAModel`` class.

Steady state calculation
''''''''''''''''''''''''

.. code-block:: python

   pm.steady_state()
   vector = pm.get_steady_state_vector()

In this case vector is a list of steady state probabilities for states [0..n]. 

Throughput
''''''''''

.. code-block:: python

   pm.steady_state()
   thr = pm.get_throughput()

Here, ``thr`` will be a list of tuples ``(action, throughput)``

Transient time analsis
''''''''''''''''''''''

.. code-block:: python

   vector = pm.transient(0, timestop)

Vector is list of probabilities.


Utlisations
'''''''''''

.. code-block:: python

   pm.steady_state()
   usabilities = pm.get_utilisations()

Here ``usabilities`` is a list of `Counter
<http://docs.python.org/3.3/library/collections.html#collections.Counter>_` objects, each being a
dict, corresponding to a component in a model, where keys are state names and values are usabilities. Example:

.. code-block:: python

   [Counter({'P1': 0.5, 'P': 0.49999999999999989}), Counter({'Q': 0.66666666666666652, 'Q1': 0.33333333333333337})]

Generating dots
'''''''''''''''

.. code-block:: python

   pm.generate_dots(out_dir=path)

This method will generate dots in a directory specified by ``path``. If this argument is not
supplied, by default dots will be generated in ``dots`` directory. 

Additional methods
''''''''''''''''''

.. method:: get_state_names()

   Returns a list of state names used for matching state number with a correponding name.
   Index of the list is the number of a state. 

.. method:: get_rates()

   Returns a dict with rate names mapped to rate values. 


