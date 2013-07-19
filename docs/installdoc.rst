Installation
============


From Package
------------

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
----------------

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


