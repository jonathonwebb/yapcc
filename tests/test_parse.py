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

from yapcc.lex import Token, TokenType
from yapcc.parse import Constant, Function, Program, Return, parse


class TestParse:
    def test_example(self) -> None:
        """Return expected AST from a simple list of tokens."""
        tokens: list[Token] = [
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

        ast = parse(tokens)

        # program node
        assert isinstance(ast, Program)

        # function node
        assert isinstance(ast.function_definition, Function)
        assert ast.function_definition.name == "main"

        # function body node
        assert isinstance(ast.function_definition.body, Return)

        # function body expression node
        assert isinstance(ast.function_definition.body.exp, Constant)
        assert ast.function_definition.body.exp.value == 2
