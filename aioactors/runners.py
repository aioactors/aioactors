from __future__ import annotations
import typing as t

import asyncio
from logging import getLogger

from .actors import Actor
from .constants import DEFAULT_TASK_TIMEOUT


class ActorSystem:
    def __init__(self, loop) -> None:
        self.logger = getLogger(type(self).__name__)
        self.loop = loop

        self.tasks: t.List[t.Coroutine] = []

    def __call__(self):
        try:
            self.start()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def start(self) -> None:
        self.logger.info("Starting...")
        self.loop.run_until_complete(asyncio.gather(*self.tasks))

    def stop(self) -> None:
        self.logger.info("Stopping...")

        for task in asyncio.all_tasks():
            self.logger.info("Stop '%s'", task)
            task.cancel()

        self.logger.info("Stop mainloop")
        self.loop.stop()
        self.loop.close()

    def add(self, task: Actor, timeout: int = DEFAULT_TASK_TIMEOUT):
        self.tasks.append(task.start(timeout))
