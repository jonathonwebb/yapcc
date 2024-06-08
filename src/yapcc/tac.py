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
"""Three-address code (TAC) intermediate representation logic."""

from dataclasses import dataclass

from yapcc.parse import ComplementOperator as ASTComplementOperator
from yapcc.parse import Constant as ASTConstant
from yapcc.parse import Expression as ASTExpression
from yapcc.parse import Function as ASTFunction
from yapcc.parse import NegateOperator as ASTNegateOperator
from yapcc.parse import Program as ASTProgram
from yapcc.parse import Return as ASTReturn
from yapcc.parse import Statement as ASTStatement
from yapcc.parse import Unary as ASTUnary
from yapcc.parse import UnaryOperator as ASTUnaryOperator


class Node:
    """Abstract TAC node."""


class Value(Node):
    """Abstract TAC value node."""


@dataclass
class Constant(Value):
    """TAC constant value node."""

    value: int


@dataclass
class Var(Value):
    """TAC constant var node."""

    value: str


class UnaryOperator(Node):
    """Abstract TAC unary operator node."""


@dataclass
class Complement(UnaryOperator):
    """TAC complement operator node."""


@dataclass
class Negate(UnaryOperator):
    """TAC negation operator node."""


class Instruction(Node):
    """Abstract TAC instruction node."""


@dataclass
class Return(Instruction):
    """TAC return instruction node."""

    value: Value


@dataclass
class Unary(Instruction):
    """TAC unary instruction node."""

    op: UnaryOperator
    src: Value
    dest: Var


@dataclass
class Function(Node):
    """TAC function node."""

    identifier: str
    body: list[Instruction]


@dataclass
class Program(Node):
    """TAC root node."""

    function_definition: Function


var_count = 0


def _create_var_name() -> str:
    global var_count
    name = "tmp_" + str(var_count)
    var_count += 1
    return name


def _transform_unop(op: ASTUnaryOperator) -> UnaryOperator:
    match op:
        case ASTNegateOperator():
            return Negate()
        case ASTComplementOperator():
            return Complement()
    raise RuntimeError("Failed to transform AST unary operator")


def _transform_ast_expression(exp: ASTExpression, instr: list[Instruction]) -> Value:
    match exp:
        case ASTConstant(v):
            return Constant(v)
        case ASTUnary(op=op, exp=inner):
            src = _transform_ast_expression(inner, instr)
            dst_name = _create_var_name()
            dst = Var(dst_name)
            tac_op = _transform_unop(op)
            instr.append(Unary(tac_op, src, dst))
            return dst
        case _:
            raise RuntimeError("Failed to transform AST expression")


def _transform_ast_statement(stat: ASTStatement) -> list[Instruction]:
    instr: list[Instruction] = []
    match stat:
        case ASTReturn(exp=exp):
            value = _transform_ast_expression(exp, instr)
            instr.append(Return(value))
        case _:
            raise RuntimeError("Failed to transform AST statement")
    return instr


def _transform_ast_function(fn: ASTFunction) -> Function:
    return Function(fn.name, _transform_ast_statement(fn.body))


def _transform_ast_program(ast: ASTProgram) -> Program:
    return Program(_transform_ast_function(ast.function_definition))


def ir(ast: ASTProgram) -> Program:
    """Accept an AST and return an intermediate three-address code representation."""
    return _transform_ast_program(ast)
