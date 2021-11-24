from __future__ import annotations

from dataclasses import dataclass, field as f


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
