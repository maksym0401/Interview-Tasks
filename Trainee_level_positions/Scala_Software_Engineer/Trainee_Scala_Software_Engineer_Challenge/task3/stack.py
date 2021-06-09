from typing import Any, List, Optional


class TSStackEmptyError(Exception):
    pass


class TSStack:

    def __init__(self, stack: Optional[List[Any]] = None):
        self._stack = stack or []

    def push(self, element: Any):
        self._stack.append(element)

    def pop(self) -> Any:
        try:
            return self._stack.pop()
        except IndexError:
            raise TSStackEmptyError('pop from empty stack') from None
