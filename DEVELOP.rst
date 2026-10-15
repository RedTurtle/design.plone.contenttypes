Development
===========

This package is configured with `plone.meta <https://github.com/plone/meta>`_.
Do not edit the generated files (``tox.ini``, ``pyproject.toml``, ``.pre-commit-config.yaml``, ...) by hand:
change ``.meta.toml`` and run::

    $ uvx --from plone.meta config-package --branch current --no-commit .

Running tests
-------------

Tests are run with `tox <https://tox.wiki>`_ (Plone 6.0, 6.1 and 6.2, Python 3.11+)::

    $ tox -l
    $ tox -e py311-plone62

Code quality
------------

    $ tox -e lint
    $ tox -e dependencies
