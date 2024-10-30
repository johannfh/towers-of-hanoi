from collections.abc import Callable
from enum import Enum
from typing import Dict, Generic, List, TypeVar, Union
import inspect

E = TypeVar("E", bound=Enum)
"""Event name type"""

D = TypeVar("D")
"""Event data type"""


Listener = Union[Callable[[], None], Callable[[D], None]]
"""
Event listener for an `EventEmitter`.

Can optionally take `D` as the first argument
"""


class EventEmitter(Generic[E, D]):
    def __init__(self):
        self._listeners: Dict[E, List[Listener[D]]] = {}
        pass

    def add_event_listener(self, event: E, listener: Listener[D]):
        """
        Attach a `Listener` function to the `EventEmitter`.

        If `Listener` is already listening to `EventEmitter`, this is a no-op.
        """

        listeners = self._listeners.get(event)

        if not listeners:
            self._listeners[event] = [listener]
            return

        if listener not in listeners:
            self._listeners[event].append(listener)

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
            # TODO: make this actually typesafe...
            sig = inspect.signature(listener)
            match len(sig.parameters):
                case 0:
                    listener()  # type: ignore
                case 1:
                    listener(data)  # type: ignore
                case _:
                    # this should never happen
                    exit()
                    assert False, f"{listener} did not match type `Listener`"
