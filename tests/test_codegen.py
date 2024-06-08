# Copyright 2024 Jon Webb <jon@jonwebb.dev>
#
# This file is part of yapcc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
"""Code generation tests for yapcc."""

import os
import subprocess
from pathlib import Path
from typing import Callable

import pytest
from yapcc.codegen import codegen, emit
from yapcc.lex import lex
from yapcc.parse import Program as ASTProgram
from yapcc.parse import parse

ParseFixture = Callable[[str], ASTProgram]


@pytest.fixture()
def parsed(tmp_path: str) -> Callable[[str], ASTProgram]:
    def _parsed(input_path: str) -> ASTProgram:
        dirname = os.path.dirname(__file__)
        input_path = os.path.join(dirname, input_path)
        preprocess_path = os.path.join(tmp_path, Path(input_path).stem) + ".i"
        subprocess.run(
            ["gcc", "-E", "-P", input_path, "-o", preprocess_path], check=True
        )
        with open(preprocess_path, "r", encoding="ascii") as preprocess_file:
            preprocessed = preprocess_file.read()
        tokens = lex(preprocessed)
        return parse(tokens)

    return _parsed


class TestLex:
    def test_valid(self, parsed: ParseFixture) -> None:
        """Return generated assembly with multi-digit constants."""
        ast = parsed("input/valid/multi_digit.c")
        expected = (
            "\t.globl main\n"
            "main:\n"
            "\tmovl\t$100, %eax\n"
            "\tret\n"
            '\t.section\t.note.GNU-stack, "",@progbits\n'
        )

        actual = emit(codegen(ast))

        assert actual == expected
