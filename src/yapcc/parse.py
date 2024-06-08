# Copyright 2024 Jon Webb <jon@jonwebb.dev>

# This file is part of yapcc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

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


class UnaryOperator(Node):
    """Abstract AST unary operator node."""


@dataclass
class ComplementOperator(UnaryOperator):
    """AST complement operator."""


@dataclass
class NegateOperator(UnaryOperator):
    """AST negate operator."""


@dataclass
class Unary(Expression):
    """AST unary expression node."""

    op: UnaryOperator
    exp: Expression


class Statement(Node):
    """Abstract AST statement node."""


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


def _peek(tokens: list[Token]) -> Token:
    if tokens:
        return tokens[0]
    else:
        raise RuntimeError("SyntaxError: unexpected end of input")


def _parse_unop(tokens: list[Token]) -> UnaryOperator:
    if _consume(tokens).type == TokenType.TILDE:
        return ComplementOperator()
    else:
        return NegateOperator()


def _parse_exp(tokens: list[Token]) -> Expression:
    next_token = _peek(tokens)
    if next_token.type == TokenType.CONSTANT:
        const_token = _consume(tokens)
        value = int(const_token.literal)
        return Constant(value)
    elif next_token.type in [TokenType.TILDE, TokenType.MINUS]:
        op = _parse_unop(tokens)
        inner_exp = _parse_exp(tokens)
        return Unary(op, inner_exp)
    elif next_token.type == TokenType.OPEN_PAREN:
        _consume(tokens)
        inner_exp = _parse_exp(tokens)
        _expect(TokenType.CLOSE_PAREN, tokens)
        return inner_exp
    else:
        raise RuntimeError(
            f'SyntaxError: Malformed expression "{tokens[0] + next_token}"'
        )


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


def _consume(tokens: list[Token]) -> Token:
    if tokens:
        return tokens.pop(0)
    else:
        raise RuntimeError("Token list is empty.")


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


def parse(tokens: list[Token]) -> Program:
    """Parse a list of tokens, returning an AST."""
    ast = Program(function_definition=_parse_function(tokens))
    if tokens:
        raise RuntimeError(
            f'SyntaxError: expected end of input, but found "{tokens[0].literal}"'
        )

    return ast
