from __future__ import annotations
import typing as t

from asyncio import BaseEventLoop, get_event_loop

from .runners import ActorSystem


class ActorApp:
    _name: str
    _map: t.Dict[str, t.Callable] = {}

    def __init__(self, name: str, *, loop: BaseEventLoop | None = None):
        self._name = name
        self._loop = loop if isinstance(loop, BaseEventLoop) else get_event_loop()

    def __call__(self, name: str) -> ActorSystem:
        return self._map[name](ActorSystem(loop=self._loop))

    def register(self, tasks: t.Dict[str, t.Callable], cleanup: bool = False) -> ActorApp:
        if cleanup:
            self._map = {}
        self._map.update(tasks)
        return self

    @property
    def name(self):
        return self._name

    def serve(self, **_):
        return self._map['server'](ActorSystem(loop=self._loop))
