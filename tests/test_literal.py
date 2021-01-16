import sys
from typing import List

import pytest

from attrs_strict import type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock

if sys.version_info < (3, 8):
    _ = pytest.importorskip("typing_extensions")
    from typing_extensions import Literal
else:
    from typing import Literal


@pytest.mark.parametrize(
    "element, type_, error_message",
    [
        pytest.param(
            "c",
            Literal["a", "b"],
            "Value of foo c is not any of the literals specified ['a', 'b']",
            id="Value not present in literal",
        ),
        pytest.param(
            2.0,
            Literal[1, 2],
            "Value of foo 2.0 is not any of the literals specified [1, 2]",
            id="2.0 == 2 but their types are not same",
        ),
        pytest.param(
            0,
            Literal[True, False],
            "Value of foo 0 is not any of the literals specified [True, False]",
            id="0 == False evalutes to True but their types are not same",
        ),
    ],
)
def test_literal_when_type_is_not_specified_raises(
    element, type_, error_message
):

    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    with pytest.raises(ValueError) as error:
        validator(None, attr, element)

    repr_msg = "<{}>".format(error_message)
    assert repr_msg == repr(error.value)


@pytest.mark.parametrize(
    "element, type_,",
    [
        pytest.param("enum-a", Literal["enum-a", "enum-b"], id="Literal match"),
        pytest.param(
            20, Literal[0x14], id="20 and 0x14 are equivalent in value and type"
        ),
        pytest.param(
            [1, 2, 3, 4, None, int, str],
            List[Literal[1, 2, 3, 4, None, int, str]],
            id="Literal part of another type",
        ),
        pytest.param(
            2,
            Literal[Literal[4], Literal[3, Literal[2]]],
            id="Combination of literals",
        ),
    ],
)
def test_literal_not_raise_for_correct_values(element, type_):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    validator(None, attr, element)
