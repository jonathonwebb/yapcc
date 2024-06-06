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

from yapcc.lex import Token, TokenType, lex


class TestLex:
    def test_empty(self) -> None:
        """Return no tokens from an empty file."""
        tokens = lex("")
        assert len(tokens) == 0

    def test_example(self) -> None:
        """Return expected tokens from a simple test file."""
        expected: list[Token] = [
            Token(TokenType.KEYWORD, "int"),
            Token(TokenType.IDENTIFIER, "main"),
            Token(TokenType.OPEN_PAREN, "("),
            Token(TokenType.KEYWORD, "void"),
            Token(TokenType.CLOSE_PAREN, ")"),
            Token(TokenType.OPEN_BRACE, "{"),
            Token(TokenType.KEYWORD, "return"),
            Token(TokenType.CONSTANT, "2"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.CLOSE_BRACE, "}"),
        ]

        tokens = lex("int main(void) {\n\treturn 2;\n}")
        assert len(tokens) == 10

        for idx, token in enumerate(tokens):
            assert token.type == expected[idx].type
            assert token.literal == expected[idx].literal
