import asyncio


class Timer:
    def __init__(self, timeout=0, callback=None, args=()):
        self._timeout = timeout
        self._callback = callback
        self._args = args
        if not (timeout == 0 and callback is None):
            # Create a real timer, otherwise create a dummy one, just for linting :(
            self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(*self._args)

    def cancel(self):
        if hasattr(self, "_task"):
            self._task.cancel()

