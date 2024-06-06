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
"""Lexer (tokenizer) step logic."""

from enum import Enum
from itertools import takewhile
from typing import NamedTuple

KEYWORDS: list[str] = ["int", "void", "return"]


class TokenType(Enum):
    """A lexical token type defined by the C standard."""

    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    CONSTANT = "constant"

    # Punctuators:
    OPEN_PAREN = "open-paren"
    CLOSE_PAREN = "close-paren"
    OPEN_BRACE = "open-brace"
    CLOSE_BRACE = "close-brace"
    SEMICOLON = "semicolon"


class Token(NamedTuple):
    """A lexed token."""

    type: TokenType
    literal: str


def _read_constant(source: str) -> Token:
    literal = "".join(takewhile(lambda char: char.isnumeric(), source))

    if len(literal) != len(source):
        next_char = source[len(literal)]
        if next_char.isalpha() or next_char == "_":
            raise RuntimeError("Identifier may not start with a digit")

    return Token(TokenType.CONSTANT, literal)


def _read_identifier(source: str) -> Token:
    literal = "".join(takewhile(lambda char: char.isalnum() or char == "_", source))

    match literal:
        case "int":
            return Token(TokenType.KEYWORD, "int")
        case "void":
            return Token(TokenType.KEYWORD, "void")
        case "return":
            return Token(TokenType.KEYWORD, "return")
        case _:
            return Token(TokenType.IDENTIFIER, literal)


def _next_token(source: str) -> tuple[Token, str]:
    match first_char := source[0]:
        case "(":
            token = Token(TokenType.OPEN_PAREN, first_char)
        case ")":
            token = Token(TokenType.CLOSE_PAREN, first_char)
        case "{":
            token = Token(TokenType.OPEN_BRACE, first_char)
        case "}":
            token = Token(TokenType.CLOSE_BRACE, first_char)
        case ";":
            token = Token(TokenType.SEMICOLON, first_char)
        case _ if first_char.isnumeric():
            token = _read_constant(source)
        case _ if first_char.isalpha() or first_char == "_":
            token = _read_identifier(source)
        case _:
            raise RuntimeError("Illegal token")

    return (token, source[len(token.literal) :])


def lex(source: str) -> list[Token]:
    """Perform lex step."""
    tokens: list[Token] = []
    while source := source.lstrip():  # strip whitespace from string start
        token, source = _next_token(source)
        tokens.append(token)
    return tokens
