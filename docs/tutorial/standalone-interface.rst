====================================
Using ZyncIO -- Standalone Interface
====================================

Now that we understand how it's possible to write code that is both sync and async, let's take a look at how ZyncIO
makes this process more ergonomic.


``@zyncio.zfunc``
=================

ZyncIO provides a number of classes that can be used as function decorators, the simplest of which is `zyncio.zfunc`:

.. testsetup::

    import asyncio
    import subprocess
    import time

    import zyncio

.. testcode::

    @zyncio.zfunc
    async def zync_sleep(zync_mode: zyncio.Mode, duration: float) -> None:
        if zync_mode is zyncio.SYNC:
            time.sleep(duration)
        else:
            await asyncio.sleep(duration)

.. doctest::

    >>> zync_sleep.call_sync(0.1)  # Runs in sync mode
    >>> asyncio.run(zync_sleep.call_async(0.1))  # Runs in async mode


Composing ZyncIO functions with ``call_zync``
---------------------------------------------

If we want to compose ZyncIO functions, we can branch on ``zync_mode``:

.. testcode::

    @zyncio.zfunc
    async def slow_print(zync_mode: zyncio.Mode, message: str) -> None:
        for c in message:
            if zync_mode is zyncio.SYNC:
                zync_sleep.call_sync(0.1)
            else:
                await zync_sleep.call_async(0.1)
            print(c, end='', flush=True)
        print()

.. doctest::
    :hide:

    >>> slow_print.call_sync('abc')
    abc
    >>> asyncio.run(slow_print.call_async('abc'))
    abc

This works, but it's verbose and error-prone. Instead, `zfunc` (and the other ZyncIO decorators we'll look at) provide
an additional method, `~zfunc.call_zync`. ``call_zync`` takes the mode as an argument, and always returns a coroutine
(so it can always be ``await``\ ed)::

    @zyncio.zfunc
    async def slow_print(zync_mode: zyncio.Mode, message: str) -> None:
        for c in message:
            await zync_sleep.call_zync(zync_mode, 0.1)
            print(c, end='', flush=True)
        print()

.. doctest::

    >>> slow_print.call_sync('Hello')
    Hello
    >>> asyncio.run(slow_print.call_async('world'))
    world

``@zyncio.zgenerator``
======================

The `zyncio.zgenerator` decorator is similar to `zfunc`, but for generator functions. It provides the same
``call_sync``, ``call_async``, and ``call_zync`` methods, but they return generators instead of coroutines:

.. testcode::

    @zyncio.zgenerator
    async def countdown(zync_mode: zyncio.Mode, start: int) -> AsyncGenerator[int]:
        for i in range(start, 0, -1):
            await zync_sleep.call_zync(zync_mode, 1.0)
            yield i

.. doctest::

    >>> for n in countdown.call_sync(3):
    ...     print(n)
    3
    2
    1

    >>> async def main() -> None:
    ...     async for n in countdown.call_async(3):
    ...         print(n)
    >>> asyncio.run(main())
    3
    2
    1

``@zyncio.zcontextmanager``
===========================

The `zyncio.zcontextmanager` decorator can be used to create context managers using generator functions, similar to
`contextlib.contextmanager`:

.. testcode::

    @zyncio.zcontextmanager
    async def run_process(zync_mode: zyncio.Mode, command: str) -> AsyncGenerator[int]:
        if zync_mode is zyncio.SYNC:
            process = subprocess.Popen(command, shell=True)
        else:
            process = await asyncio.create_subprocess_shell(command)

        print('Process started.')

        try:
            yield process.pid
        finally:
            process.terminate()
            if zync_mode is zyncio.SYNC:
                process.wait()
            else:
                await process.wait()


            print('Process terminated.')

.. doctest::

    >>> with run_process.call_sync('sleep 60') as pid:
    ...     print('PID:', pid)
    Process started.
    PID: ...
    Process terminated.

    >>> async def main() -> None:
    ...     async with run_process.call_async('sleep 60') as pid:
    ...         print('PID:', pid)
    >>> asyncio.run(main())
    Process started.
    PID: ...
    Process terminated.

---

These decorators are useful, but we'll introduce the real magic of ZyncIO in the next chapter:
:doc:`class-based-interface`.
