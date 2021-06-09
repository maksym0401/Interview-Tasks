from typing import Any

import pytest
from task3.stack import TSStack, TSStackEmptyError


@pytest.mark.parametrize('element', [
    2, 'string', [2, 4, 'string', ()], (TSStack(),),
])
def test_stack_supporting_diferent_data_types(element: Any):
    stack = TSStack()

    stack.push(element)
    poped_element = stack.pop()
    assert element == poped_element


def test_raise_exc_when_pop_from_empty_stack():
    stack = TSStack()
    with pytest.raises(TSStackEmptyError):
        stack.pop()

    stack.push('el')
    stack.pop()
    with pytest.raises(TSStackEmptyError):
        stack.pop()
