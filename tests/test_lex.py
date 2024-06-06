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
"""Lexer tests for yapcc."""

import os
import subprocess
from pathlib import Path
from typing import Callable

import pytest
from yapcc.lex import Token, TokenType, lex

PreprocessFixture = Callable[[str], str]
AssertTokensFixture = Callable[[list[Token], list[Token]], None]


@pytest.fixture()
def preprocess(tmp_path: str) -> Callable[[str], str]:
    def _preprocess(input_path: str) -> str:
        dirname = os.path.dirname(__file__)
        input_path = os.path.join(dirname, input_path)
        preprocess_path = os.path.join(tmp_path, Path(input_path).stem) + ".i"
        subprocess.run(
            ["gcc", "-E", "-P", input_path, "-o", preprocess_path], check=True
        )
        with open(preprocess_path, "r", encoding="ascii") as preprocess_file:
            return preprocess_file.read()

    return _preprocess


@pytest.fixture()
def assert_tokens() -> Callable[[list[Token], list[Token]], None]:
    def _assert_tokens(actual: list[Token], expected: list[Token]) -> None:
        assert len(actual) == len(expected)

        for idx, token in enumerate(actual):
            assert token.type == expected[idx].type
            assert token.literal == expected[idx].literal

    return _assert_tokens


class TestLex:
    def test_valid_multi_digit(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with multi-digit constants."""
        source = preprocess("input/valid/multi_digit.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "100"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_newlines(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with newlines."""
        source = preprocess("input/valid/newlines.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_no_newlines(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens without newlines."""
        source = preprocess("input/valid/no_newlines.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_return_0(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with return value integer 0."""
        source = preprocess("input/valid/return_0.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_return_2(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with return value integer 2."""
        source = preprocess("input/valid/return_2.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "2"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_spaces(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with spaces."""
        source = preprocess("input/valid/spaces.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_valid_tabs(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens with tabs."""
        source = preprocess("input/valid/tabs.c")
        expected: list[Token] = [
            Token(TokenType.INT_KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.VOID_KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.RETURN_KEYWORD, "return"),
            Token(TokenType.CONSTANT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        actual = lex(source)

        assert_tokens(actual, expected)

    def test_invalid_at_sign(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Raise expected error with illegal "@" sign."""
        source = preprocess("input/invalid_lex/at_sign.c")
        with pytest.raises(RuntimeError, match='TokenError: Illegal token "@"'):
            lex(source)

    def test_invalid_backtick(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Raise expected error with illegal "`" character."""
        source = preprocess("input/invalid_lex/backtick.c")
        with pytest.raises(RuntimeError, match='TokenError: Illegal token "`"'):
            lex(source)

    def test_invalid_identifier(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Raise expected error when an identifier starts with a digit."""
        source = preprocess("input/invalid_lex/invalid_identifier.c")
        with pytest.raises(RuntimeError, match='TokenError: Illegal token "@"'):
            lex(source)

    def test_invalid_identifier_2(
        self, preprocess: PreprocessFixture, assert_tokens: AssertTokensFixture
    ) -> None:
        """Return expected tokens when an identifier starts with a non-alphanumeric character."""
        source = preprocess("input/invalid_lex/invalid_identifier_2.c")
        with pytest.raises(RuntimeError, match='TokenError: Illegal constant "1f..."'):
            lex(source)
