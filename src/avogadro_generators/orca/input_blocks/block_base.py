# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Base classes and functions for input blocks in ORCA."""

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import NewType

"""Strings that are specially recognized by ORCA, for example in the
%method block you can use ``method HF`` and it will be recognized
without needing double quotes around ``HF``.
"""
ORCAString = NewType("ORCAString", str)


@dataclass(frozen=True)
class BlockKeyword:
    """Base class for input block keywords.

    Attributes
    ----------
    key_name : str
        Keyword name.
    _dtype : ORCAString or str or bool or int or float or Sequence or dict
        Type of the variable, controls formatting in the input.
    default : _dtype or int, optional
        The default value of the keyword or the index of it in ``options``.

        If ``options`` exists, then this is the index of the default
        option. For example, if ``options=("CG", "DIIS", "Pople")`` then
        setting ``default=2`` means the default is ``"Pople"``.
    options : tuple of dtype, optional
        Tuple of known options for the keyword if they exist.
    minimum : int or float, optional
        The minimum possible value.
    maximum : int or float, optional
        The maximum possible value.
    """

    key_name: str
    _dtype: (
        type[ORCAString]
        | type[str]
        | type[bool]
        | type[int]
        | type[float]
        | type[Sequence]
        | type[dict]
    )
    default: ORCAString | str | bool | int | float | Sequence | dict | None = None
    options: tuple[ORCAString | str | bool | int | float | Sequence | dict] | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None

    @property
    def dtype(self) -> str:
        if self._dtype is ORCAString or self._dtype is str:
            if self.options is not None:
                return "stringList"
            else:
                return "string"
        elif self._dtype is bool:
            return "boolean"
        elif self._dtype is int:
            return "integer"
        elif self._dtype is float:
            return "float"
        elif self._dtype is Sequence or self._dtype is dict:
            return "string"
        else:
            raise ValueError(
                f"Invalid Type {self._dtype} for BlockEnum member {self}.\n"
                "How did you even get here?"
            )

    def is_default(self, value) -> bool:
        """Determine whether or not a value is the default for the
        keyword. If there is no default, this will return ``False`` for
        anything that is an empty value.

        Notes
        -----
        A keyword that is a sequence or dict should probably never have
        a default.
        """
        if isinstance(value, str) and value == "":
            return True

        if self.default is None:
            if isinstance(value, (str, Sequence, dict)):
                if len(value) == 0:  # Empty strings or sequences are the default
                    return True
            elif isinstance(value, (int, float, bool)):
                return False  # If it is a number it must exist.
        else:
            if isinstance(value, (bool, int, float)):
                return value == self.default
            elif isinstance(value, str):
                if isinstance(self.options, Sequence):
                    return value == self.options[self.default]
                else:
                    return value == self.default
        raise RuntimeError(
            f"Something went wrong with checking the default for {self} against {value}."
        )


class BlockEnum(BlockKeyword, Enum):
    """Base class for block keyword enums."""

    def __new__(
        cls,
        key_name: str,
        _dtype: ORCAString | str | bool | int | float | Sequence,  # noqa: FBT001, PYI041
        default: ORCAString | str | bool | int | float | Sequence | None = None,  # noqa: FBT001, PYI041
        options: tuple[ORCAString | str | bool | int | float | Sequence] | None = None,
        minimum: int | float | None = None,  # noqa: PYI041
        maximum: int | float | None = None,  # noqa: PYI041
    ):
        self = BlockKeyword.__new__(cls)
        self._value_ = key_name
        return self

    def __str__(self) -> str:
        return self.key_name

    # def __repr__(self) -> str:
    #     """Returns, e.g., 'ElProp.Dipole'."""
    #     return f"{self.__class__.__name__}.{self.name}"

    def get_json_key(self) -> str:
        """Give the JSON key we will use."""
        return f"{self.__class__.__name__}_{self.name}"


class NestedBlockEnum(BlockKeyword, Enum):
    """Class for handling nested blocks, such as the TRAH section of %scf.

    Currently unused.
    """

    def __new__(
        cls,
        key_name: str,
        _dtype: ORCAString | str | bool | int | float | Sequence,  # noqa: FBT001, PYI041
        default: ORCAString | str | bool | int | float | Sequence | None = None,  # noqa: FBT001, PYI041
        options: tuple[ORCAString | str | bool | int | float | Sequence] | None = None,
        minimum: int | float | None = None,  # noqa: PYI041
        maximum: int | float | None = None,  # noqa: PYI041
    ):
        self = BlockKeyword.__new__(cls)
        self._value_ = key_name
        return self


def format_block_keyword(
    kwd: BlockKeyword,
    val: str | bool | int | float | Sequence,  # noqa: FBT001, PYI041
) -> str:

    if kwd._dtype is str:
        return f'    {kwd} = "{val}"\n'
    elif kwd._dtype is Sequence:
        fmt = f"    {kwd} = "
        for item in val[:-1]:
            fmt += f"{item}, "
        fmt += f"{val[-1]}\n"
        return fmt
    else:
        return f"    {kwd} = {val}\n"
