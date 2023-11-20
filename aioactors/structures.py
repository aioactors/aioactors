from __future__ import annotations

import typing as t

from dataclasses import dataclass
from dataclasses import field as f

from .constants import JITTER_END, JITTER_START


@dataclass
class MessageCounter:
    _error: int = f(default=0)
    _ok: int = f(default=0)
    _skip: int = f(default=0)

    def success(self) -> None:
        self._ok += 1

    def error(self) -> None:
        self._error += 1

    def skip(self) -> None:
        self._skip += 1

    def flush(self) -> MessageCounter:
        self._ok = 0
        self._error = 0
        self._skip = 0
        return self

    @property
    def total(self):
        return self._ok + self._error + self._skip

    def __bool__(self):
        return self.total > 0

    def __str__(self):
        return f"Messages (ok={self._ok}, skip={self._skip}, error={self._error})"


@dataclass
class Jitter:
    start: int = f(default=JITTER_START)
    end: int = f(default=JITTER_END)

    change: t.Callable[[int], int] = f(default=lambda t: 2**t)

    _value: int = f(default=0)
    _step: int = f(default=0)

    def step(self) -> None:
        if self._value == self.end:
            return

        self._value = self.calculate()
        self._step += 1
        if self._value > self.end:
            self._value = self.end
            self._step -= 1

    def calculate(self):
        return self.change(self._step)

    def drop(self) -> None:
        self._value = self.start

    @property
    def value(self) -> int:
        return self._value
