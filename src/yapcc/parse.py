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
"""Recursive descent parser logic."""

from dataclasses import dataclass

from yapcc.lex import Token, TokenType


class Node:
    """Abstract AST node."""


class Expression(Node):
    """Abstract AST expression node."""


@dataclass
class Constant(Expression):
    """AST constant expression node."""

    value: int


class Statement(Node):
    """AST abstract statement node."""


@dataclass
class Return(Statement):
    """AST return statement node."""

    exp: Expression


@dataclass
class Function(Node):
    """AST function node."""

    name: str
    body: Statement


@dataclass
class Program(Node):
    """AST root node."""

    function_definition: Function


AST = Node


def _parse_exp(tokens: list[Token]) -> Expression:
    const_token = _expect(TokenType.CONSTANT, tokens)
    value = int(const_token.literal)
    return Constant(value=value)


def _parse_statement(tokens: list[Token]) -> Statement:
    _expect(TokenType.RETURN_KEYWORD, tokens)
    return_val = _parse_exp(tokens)
    _expect(TokenType.SEMICOLON, tokens)
    return Return(exp=return_val)


def _parse_function(tokens: list[Token]) -> Function:
    _expect(TokenType.INT_KEYWORD, tokens)
    ident_token = _expect(TokenType.IDENTIFIER, tokens)
    name = ident_token.literal
    _expect(TokenType.OPEN_PAREN, tokens)
    _expect(TokenType.VOID_KEYWORD, tokens)
    _expect(TokenType.CLOSE_PAREN, tokens)
    _expect(TokenType.OPEN_BRACE, tokens)
    body = _parse_statement(tokens)
    _expect(TokenType.CLOSE_BRACE, tokens)

    return Function(name=name, body=body)


def _expect(expected: TokenType, tokens: list[Token]) -> Token:
    if tokens:
        actual = tokens.pop(0)
        if actual.type != expected:
            raise RuntimeError(
                f'SyntaxError: expected {expected}, but found "{actual.literal}"'
            )
    else:
        raise RuntimeError(f"SyntaxError: expected {expected}, but found end of input")
    return actual


def parse(tokens: list[Token]) -> AST:
    """Parse a list of tokens, returning an AST."""
    ast = Program(function_definition=_parse_function(tokens))
    if tokens:
        raise RuntimeError(
            f'SyntaxError: expected end of input, but found "{tokens[0].literal}"'
        )

    return ast
