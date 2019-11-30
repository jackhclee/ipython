"""
Inputhook for running the original asyncio event loop while we're waiting for
input.

By default, in IPython, we run the prompt with a different asyncio event loop,
because otherwise we risk that people are freezing the prompt by scheduling bad
coroutines. E.g., a coroutine that does a while/true and never yield back
control to the loop. We can't cancel that.

However, sometimes we want the asyncio loop to keep running while waiting for
a prompt.

The following example will print the numbers from 1 to 10 above the prompt,
while we are waiting for input. (This works also because we use
prompt_toolkit`s `patch_stdout`)::

    In [1]: import asyncio

    In [2]: %gui asyncio

    In [3]: async def f():
       ...:     for i in range(10):
       ...:         await asyncio.sleep(1)
       ...:         print(i)


    In [4]: asyncio.ensure_future(f())

"""
import asyncio

# Keep reference to the original asyncio loop, because getting the event loop
# within the input hook would return the other loop.
loop = asyncio.get_event_loop()


def inputhook(context):
    def stop():
        loop.stop()

    loop.add_reader(context.fileno(), stop)
    context.fileno()
    loop.run_forever()