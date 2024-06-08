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
"""Assembly codegen step logic."""

from dataclasses import dataclass

from yapcc.parse import Constant as ASTConstant
from yapcc.parse import Function as ASTFunction
from yapcc.parse import Program as ASTProgram
from yapcc.parse import Return as ASTReturn
from yapcc.parse import Statement as ASTStatement


class Node:
    """Abstract assembly node."""


class Operand(Node):
    """Abstract assembly operand."""


class Expression(Operand):
    """Abstract assembly expression."""


@dataclass
class Imm(Expression):
    """Assembly imm expression."""

    value: int


class Register(Operand):
    """Assembly register."""


class Instruction(Node):
    """Abstract assembly instruction."""


@dataclass
class Mov(Instruction):
    """Assembly mov instruction."""

    src: Imm
    dest: Register


class Ret(Instruction):
    """Assembly ret instruction."""


@dataclass
class Function(Node):
    """Assembly function node."""

    name: str
    instructions: list[Instruction]


@dataclass
class Program(Node):
    """Assembly root node."""

    function_definition: Function


def _transform_ast_constant(c: ASTConstant) -> Imm:
    return Imm(c.value)


def _transform_ast_statement(s: ASTStatement) -> list[Instruction]:
    if isinstance(s, ASTReturn):
        if isinstance(s.exp, ASTConstant):
            return [Mov(_transform_ast_constant(s.exp), Register()), Ret()]
        else:
            raise RuntimeError(
                f'Unsupported AST return expression "${type(s).__name__}"'
            )
    else:
        raise RuntimeError(f'Unsupported AST statement "${type(s).__name__}"')


def _transform_ast_function(ast_function: ASTFunction) -> Function:
    return Function(
        name=ast_function.name,
        instructions=_transform_ast_statement(ast_function.body),
    )


def _transform_program(ast: ASTProgram) -> Program:
    return Program(function_definition=_transform_ast_function(ast.function_definition))


def codegen(ast: ASTProgram) -> Program:
    """Transform an AST, returning an intermediate assembly tree."""
    program = _transform_program(ast)
    return program


def emit(program: Program) -> str:
    """Format an intermediate assembly tree."""
    output: list[str] = []

    fn = program.function_definition
    output.append(f"\t.globl {fn.name}")
    output.append(f"{fn.name}:")
    for instr in fn.instructions:
        if isinstance(instr, Mov):
            output.append(f"\tmovl\t${instr.src.value}, %eax")
        elif isinstance(instr, Ret):
            output.append("\tret")

    output.append('\t.section\t.note.GNU-stack, "",@progbits\n')
    return "\n".join(output)
