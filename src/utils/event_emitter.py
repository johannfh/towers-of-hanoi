from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Dict, Generic, List, Optional, TypeVar

E = TypeVar("E", bound=Enum)
"""Event name type"""

D = TypeVar("D")
"""Event data type"""

Listener = Callable[[D], None]
"""Event listener for an `EventEmitter`"""


class EventEmitter(Generic[E, D]):
    def __init__(self):
        self._listeners: Dict[E, List[Listener[D]]]
        pass

    def add_event_listener(self, event: E, listener: Listener[D]):
        """
        Attach a `Listener` function to the `EventEmitter`.

        If `Listener` is already listening to `EventEmitter`, this is a no-op.
        """

        listeners = self._listeners.get(event)

        if not listeners:
            self._listeners[event].append(listener)
            return

        if listener not in listeners:
            listeners.append(listener)
            pass

    def remove_event_listener(self, event: E, listener: Listener[D]):
        """
        Remove a `Listener` function from the `EventEmitter`,
        if it is currently subscribed to the `event`.
        """

        listeners = self._listeners.get(event)

        if listeners and listener in listeners:
            listeners.remove(listener)

    def emit(self, event: E, data: D):
        """
        Notify all `Listener` functions that `event`
        occured with the provided `data`.
        """

        listeners = self._listeners.get(event)

        if not listeners:
            return

        for listener in listeners:
            listener(data)
