:tocdepth: 3

==============
Standalone API
==============

The standalone API lets you write ZyncIO code that's not tied to a class.

.. currentmodule:: zyncio


Decorators
==========

.. autoclass:: zfunc
    :members:

.. autoclass:: zgenerator

    .. automethod:: call_async
        :async-for:

    .. automethod:: call_sync
        :for:

    .. automethod:: call_zync
        :async-for:

.. autoclass:: zcontextmanager

    .. automethod:: call_async
        :async-with:

    .. automethod:: call_sync
        :with:

    .. automethod:: call_zync
        :async-with:
