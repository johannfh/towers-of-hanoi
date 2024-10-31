from typing import Generic, List, TypeVar


T = TypeVar("T")


class Queue(Generic[T]):
    """
    A really simple generic **Queue** implementation. Learn more about Queues at:

    https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
    """

    _items: List[T]
    """Items in this `Queue`"""

    def __init__(self):
        self._items = []

    def enqueue(self, *items: T) -> None:
        """Add new items to this `Queue`."""
        for item in items:
            self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the next element in `Queue`.
        Raises `IndexError` if the `Queue` is empty."""
        return self._items.pop(0)

    def peek(self) -> T:
        """Return the next element in `Queue` without removing it.
        Raises `IndexError` if the `Queue` is empty."""
        return self._items[0]

    def empty(self) -> bool:
        """Check if this `Queue` is empty."""
        return len(self) == 0

    def clear(self) -> List[T]:
        """Remove and return **ALL** items from this `Queue`."""
        items = self._items
        self._items = []
        return items

    def __len__(self) -> int:
        """Return the number of items in this `Queue`."""
        return len(self._items)
