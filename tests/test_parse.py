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
"""Parser tests for yapcc."""

import os
import subprocess
from pathlib import Path
from typing import Callable

import pytest
from yapcc.lex import Token, lex
from yapcc.parse import (
    ComplementOperator,
    Constant,
    Function,
    NegateOperator,
    Node,
    Program,
    Return,
    Unary,
    parse,
)

LexedFixture = Callable[[str], list[Token]]


@pytest.fixture()
def lexed(tmp_path: str) -> Callable[[str], list[Token]]:
    def _lexed(input_path: str) -> list[Token]:
        dirname = os.path.dirname(__file__)
        input_path = os.path.join(dirname, input_path)
        preprocess_path = os.path.join(tmp_path, Path(input_path).stem) + ".i"
        subprocess.run(
            ["gcc", "-E", "-P", input_path, "-o", preprocess_path], check=True
        )
        with open(preprocess_path, "r", encoding="ascii") as preprocess_file:
            preprocessed = preprocess_file.read()
            return lex(preprocessed)

    return _lexed


class TestParse:
    def test_valid(self, lexed: LexedFixture) -> None:
        """Return expected AST with valid syntax."""
        tokens = lexed("input/valid/multi_digit.c")

        actual: Node = parse(tokens)

        # program node
        assert isinstance(actual, Program)

        # function node
        assert isinstance(actual.function_definition, Function)
        assert actual.function_definition.name == "main"

        # function body node
        assert isinstance(actual.function_definition.body, Return)

        # function body expression node
        assert isinstance(actual.function_definition.body.exp, Constant)
        assert actual.function_definition.body.exp.value == 100

    def test_valid_nested_exp(self, lexed: LexedFixture) -> None:
        """Return expected AST with nested unary expressions."""
        tokens = lexed("input/valid/nested_exp.c")

        actual = parse(tokens)

        # program node
        program = actual
        assert isinstance(program, Program)

        # function node
        fn = program.function_definition
        assert isinstance(fn, Function)
        assert fn.name == "main"

        # function body node
        body = fn.body
        assert isinstance(body, Return)

        # function body expression node
        exp = body.exp
        assert isinstance(exp, Unary)
        assert isinstance(exp.op, ComplementOperator)

        # nested expression node
        nested_exp = exp.exp
        assert isinstance(nested_exp, Unary)
        assert isinstance(nested_exp.op, NegateOperator)

        # leaf constant node
        constant = nested_exp.exp
        assert isinstance(constant, Constant)
        assert constant.value == 1

    def test_invalid_end_before_expr(self, lexed: LexedFixture) -> None:
        """Raises expected error with unterminated expressions."""
        tokens = lexed("input/invalid_parse/end_before_expr.c")
        with pytest.raises(
            RuntimeError,
            match="SyntaxError: unexpected end of input",
        ):
            parse(tokens)

    def test_invalid_extra_junk(self, lexed: LexedFixture) -> None:
        """Raises expected error with extra junk."""
        tokens = lexed("input/invalid_parse/extra_junk.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected end of input, but found "foo"',
        ):
            parse(tokens)

    def test_invalid_function_name(self, lexed: LexedFixture) -> None:
        """Raises expected error with invalid function names."""
        tokens = lexed("input/invalid_parse/invalid_function_name.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.IDENTIFIER, but found "3"',
        ):
            parse(tokens)

    def test_invalid_keyword_wrong_case(self, lexed: LexedFixture) -> None:
        """Raises expected error with wrongly cased keywords."""
        tokens = lexed("input/invalid_parse/keyword_wrong_case.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.RETURN_KEYWORD, but found "RETURN"',
        ):
            parse(tokens)

    def test_invalid_missing_type(self, lexed: LexedFixture) -> None:
        """Raises expected error missing function types."""
        tokens = lexed("input/invalid_parse/missing_type.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.INT_KEYWORD, but found "main"',
        ):
            parse(tokens)

    def test_invalid_misspelled_keyword(self, lexed: LexedFixture) -> None:
        """Raises expected error with misspelled keywords."""
        tokens = lexed("input/invalid_parse/misspelled_keyword.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.RETURN_KEYWORD, but found "returns"',
        ):
            parse(tokens)

    def test_invalid_missing_semicolon(self, lexed: LexedFixture) -> None:
        """Raises expected error with missing semicolons."""
        tokens = lexed("input/invalid_parse/no_semicolon.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.SEMICOLON, but found "}"',
        ):
            parse(tokens)

    def test_invalid_not_expression(self, lexed: LexedFixture) -> None:
        """Raises expected error when semicolon terminates a non-expression."""
        tokens = lexed("input/invalid_parse/not_expression.c")
        with pytest.raises(
            RuntimeError,
            match="SyntaxError: Malformed expression",
        ):
            parse(tokens)

    def test_invalid_space_in_keyword(self, lexed: LexedFixture) -> None:
        """Raises expected error with space in keywords."""
        tokens = lexed("input/invalid_parse/extra_junk.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected end of input, but found "foo"',
        ):
            parse(tokens)

    def test_invalid_switched_parens(self, lexed: LexedFixture) -> None:
        """Raises expected when parentheses direction is inverted."""
        tokens = lexed("input/invalid_parse/switched_parens.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.OPEN_PAREN, but found "\\)"',
        ):
            parse(tokens)

    def test_invalid_unclosed_brace(self, lexed: LexedFixture) -> None:
        """Raises expected error when braces are left unclosed."""
        tokens = lexed("input/invalid_parse/unclosed_brace.c")
        with pytest.raises(
            RuntimeError,
            match="SyntaxError: expected TokenType.CLOSE_BRACE, but found end of input",
        ):
            parse(tokens)

    def test_invalid_unclosed_paren(self, lexed: LexedFixture) -> None:
        """Raises expected error when parentheses are left unclosed."""
        tokens = lexed("input/invalid_parse/unclosed_paren.c")
        with pytest.raises(
            RuntimeError,
            match='SyntaxError: expected TokenType.CLOSE_PAREN, but found "{"',
        ):
            parse(tokens)
