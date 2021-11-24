import asyncio
from logging import getLogger, Logger
from abc import abstractmethod, ABC
from time import monotonic

from .structures import MessageCounter
from .constants import (
    DEFAULT_TASK_TIMEOUT,
    DEFAULT_STATISTIC_INTERVAL
)


class Actor(ABC):
    logger: Logger = getLogger()

    def __new__(cls, *_, **kwargs):
        obj = super().__new__(cls)

        obj.logger = cls.logger.getChild(f'{cls.__name__}')

        if '_id' in kwargs:
            obj.id = kwargs['_id']
            obj.logger = obj.logger.getChild(str(kwargs['_id']))

        return obj

    @abstractmethod
    async def __call__(self) -> None:
        raise NotImplementedError()

    async def start(self, timeout: int = DEFAULT_TASK_TIMEOUT) -> None:
        while True:
            await self()
            await asyncio.sleep(timeout)

    async def wait(self, timeout: float = None) -> None:
        return await asyncio.sleep(timeout if isinstance(timeout, int) and timeout > 0 else 0)


class ActorWithStatistic(Actor, ABC):
    statistic_at: float = DEFAULT_STATISTIC_INTERVAL

    _counter: MessageCounter
    _start_at: float
    _results_at: float

    def __new__(cls, *_, **__):
        obj = super().__new__(cls)

        obj._counter = MessageCounter()
        obj._start_at = monotonic()
        obj._results_at = obj._start_at + obj.statistic_at  # pylint: disable=no-member

        return obj

    @abstractmethod
    async def __call__(self) -> None:
        raise NotImplementedError()

    async def wait(self, timeout: float = None) -> None:
        if (now := monotonic()) > self._results_at:
            self.logger.info("%s - [Running: %sms]", self._counter, round(now - self._start_at, 0))
            self._counter.flush()
            self._results_at = self._results_at + self.statistic_at

        return await super().wait(timeout)
