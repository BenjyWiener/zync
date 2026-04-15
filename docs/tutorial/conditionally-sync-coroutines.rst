=============================
Conditionally-Sync Coroutines
=============================

We've introduced the concept of sync coroutines, but they aren't particularly useful on their own.
What good is a coroutine if it can't actually do any asynchronous work?

That brings us to our next concept: conditionally-sync coroutines.

We can define an ``async`` function that has two code paths: one that exclusively performs synchronous
work, and another that performs asynchronous work:

.. testsetup::

    import asyncio
    import time

    import zyncio

.. testcode::

    async def zync_sleep(duration: float, *, sync: bool) -> None:
        if sync:
            # Synchronous code path
            time.sleep(duration)
        else:
            # Asynchronous code path
            await asyncio.sleep(duration)

Now, we can can execute the synchronous code path using `zyncio.run_sync`:

.. doctest::

    >>> zyncio.run_sync(zync_sleep(0.1, sync=True))

... but the asynchronous code path still requires an event loop:

.. doctest::

    >>> zyncio.run_sync(zync_sleep(0.1, sync=False))
    Traceback (most recent call last):
      ...
    RuntimeError: ZyncIO functions must only await pure coroutines in sync mode
    >>> asyncio.run(zync_sleep(0.1, sync=False))  # ... but this works

We now have a way to write functions that are both sync and async, where any code that isn't sync/async
specific can be shared.

Next: :doc:`standalone-interface`
