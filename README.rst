pypepa
------

.. image:: https://raw.github.com/tdi/pypepa/dev/docs/pypepa.png

pypepa is a PEPA library and a toolset for `Performance Evaluation Process Algebra <http://www.dcs.ed.ac.uk/pepa/>`_ (PEPA) by Jane
Hillston. pyPEPA is not a fully PEPA compatible tool, it supports a limited (for now) PEPA syntax (we only allow ``<>`` operator in system equation), i.e. it does not suport hiding operator (e.g. ``P\{a,b,}``), does not calculate passage time. pyPEPA also does not use Kronecker state space representation and Hillston's aggregation algorithms, so it can have worse performance than the PEPA Eclipse Plugin.
All these features, plus more, are planned to be added in next versions. If you are willing to help, just email me or put a pull request. 

**Warning: pyPEPA is under development, this is a beta software**

pyPEPA consist of three parts:

1. libpepa - a library written in Python,
2. pyPEPA - a command line tool for solving and graphing,
3. distr/ - map reduce tools for solving large PEPA experiments.

More docs can be found on `readthedocs <https://pypepa.readthedocs.org/en/latest/>`_.


News
----
(22.07.2013) Docs added, pypepa has now docs on rtd.org
(18.07.2013) pypepa can now calculate utilisations of components' states, output argument works
again
(07.06.2013) Added support for defining rates as mathematical expressions, e.g. r=2*3+7*n;

Installation
------------

Package
~~~~~~~
Using pip:

.. code-block:: bash

   $ pip install pypepa

Manually:

1. Clone the project

.. code-block:: bash

    $ git clone git@github.com:tdi/pyPEPA.git pypepa
    $ cd pypepa

2. Run install

.. code-block:: bash

    $ python setup.py install


From the source
~~~~~~~~~~~~~~~~

For the current version I recommend installing in a virtualenv. 

1. Clone the project

.. code-block:: bash

    $ git clone git@github.com:tdi/pyPEPA.git pypepa
    $ cd pypepa

2. Make a virtualenv

.. code-block:: bash

    $ mkvirtualenv -p /usr/bin/python3 pypepa
    $ workon pypepa

3. Install all requirements

.. code-block:: bash

    $ pip install pyparsing numpy scipy matplotlib


Using pypepa
------------

Basic arguments
~~~~~~~~~~~~~~~

Show help command:

.. code-block:: bash

     $ pypepa -h

Set logging level (the default is NONE):

.. code-block:: bash

    $ pypepa --log {DEBUG, INFO, ERROR, NONE}
   
Calculations
~~~~~~~~~~~~

Calculate steady state for bank scenario. The putput is by default directed to your terminal. 

.. code-block:: bash

    $ pypepa -st models/bankscenario.pepa
    
    Statespace of models/bankscenario.pepa.1 has 7 states 
    
    Steady state vector
    Using ; delimiter
    1;Idle,WaitingForCustomer,WaitingForEmployee;0.08333333333333337
    2;Informed,WaitingForCustomer,WaitingForEmployee;0.25
    3;WaitingBankResponse,RequestReceived,WaitingForEmployee;0.16666666666666666
    4;WaitingBankResponse,CustomerNotReliable,WaitingForEmployee;0.16666666666666666
    5;WaitingBankResponse,CustomerReliable,WaitingForEmployee;0.16666666666666666
    6;WaitingBankResponse,WaitingManagerResponse,EvaluatingOffer;0.08333333333333333
    7;OfferReceived,WaitingForCustomer,WaitingForEmployee;0.08333333333333333
    
Calculate actions' throughput:

.. code-block:: bash

    $ pypepa -th models/bankscenario.pepa
    
    Statespace of models/bankscenario.pepa.1 has 7 states 

    Throuhput (successful action completion in one time unit)
    
    readInformation                          0.08333333333333337
    createLoanRequest                              0.25
    getNotReliableMessage                    0.16666666666666666
    badOffer                                 0.08333333333333333
    askManager                               0.16666666666666666
    reset                                    0.08333333333333333
    goodOffer                                0.08333333333333333
    checkReliability                         0.3333333333333333
    
You can calculate transient time proability for some number of time steps:

.. code-block:: bash

    $ pypepa --transient 5 models/bankscenario.pepa
    
    Transient analysis from time 0 to 10

    Using ; delimiter
    1;Idle,WaitingForCustomer,WaitingForEmployee;0.08351202761947342
    2;Informed,WaitingForCustomer,WaitingForEmployee;0.2500169897974121
    3;WaitingBankResponse,RequestReceived,WaitingForEmployee;0.16662129023697114
    4;WaitingBankResponse,CustomerNotReliable,WaitingForEmployee;0.16657721277634494
    5;WaitingBankResponse,CustomerReliable,WaitingForEmployee;0.16657721277634485
    6;WaitingBankResponse,WaitingManagerResponse,EvaluatingOffer;0.08328947039778702
    7;OfferReceived,WaitingForCustomer,WaitingForEmployee;0.08340579639566591
    
You can choose a solver by specifying ``--solver|-s {direct, sparse}``. 
By defalt we use sparse solver with LIL matrix becuase it is faster and in overall matrices generated from PEPA models are sparse. There is also an insignificant difference in results. 

pypepa allows you to visualise all PEPA components and the whole state space of a model by specifying ``-gd`` switch. The generated graphiz dot files are by deault saved in ``dots`` folder in the current directory. You can browse dot files with ``xdot``, which you need to install first. 

.. code-block:: bash

    $ pypepa -gd bankdots models/bankscenario.pepa


Finally pypepa can provide us with a tool for experimentation with rates and actions. 
Let's check how throughtput of ``askManager`` action changes when ``rateReset`` changes from 1 to 50 with step 1. The default result of this command will be a matplotlib graph.
The format of ``-var`` is "vartype:varname:value range specifier:value range value". The one valid
vartype for now is ``rate``, for value range specifiers you can choose: ``range`` or ``list``. For ``range``
you need to provide START, STOP, STEP, whereas for ``list`` a comma separated list of values. 
You can specify other output options with ``-f`` argument: graph, console, csv. 

.. code-block:: bash

    $ pypepa -var "rate:rateReset:range:1,50,1" -val askManager  models/bankscenario.pepa

.. image:: https://raw.github.com/tdi/pypepa/dev/docs/bankexample.png
   :width: 350pt 


Formatting
~~~~~~~~~~

You can specify formats of ``-st``, ``-th`` and  ``--varrate`` with a ``--format`` option. 
Currently we support CSV (although `;` not comma delimited), console (the default) and graph (only
for varrate experiments). Additionally you can specify ``-o|--output`` option with a file argument to specify where to save the CSV. 

.. code-block:: bash

    $ pypepa -st models/bankscenario.pepa -f csv -o bank_steady.csv


TODO
----

Functional
~~~~~~~~~~

1. Implement rate mathematical expressions with functional rates (DONE)
2. Implement passage time analysis
3. Implement hiding operator
4. Implement 3d graphs and experiments (DONE)
5. Implement Kronecker state space and aggregation
6. Implement generalised communication PEPA `genPEPA <http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=6354646>`_  by Mirco Tribastone
7. Add model manipulation language for reducers
8. Add stochastic probes
9. Add distributed version of BU algorithm

Non functional
~~~~~~~~~~~~~~

1. Optimise optimise optimise

Licence and credits
-------------------

Copyright (c) Dariusz Dwornikowski and Poznan University of Technology. 
Distributed under the Apache Commons 2.0. 


