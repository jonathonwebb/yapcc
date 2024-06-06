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
"""Main CLI entrypoint."""

import argparse
import contextlib
import os
import subprocess
import sys
from pprint import pp
from typing import Callable

from yapcc.lex import lex
from yapcc.parse import parse


def _make_cleanup(paths: list[str]) -> Callable[[], None]:
    def cleanup() -> None:
        for f in paths:
            with contextlib.suppress(FileNotFoundError):
                os.remove(f)

    return cleanup


def main() -> None:
    """Run compiler CLI."""
    parser = argparse.ArgumentParser(description="Yet Another Python C Compiler")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lex", action="store_true", help="lex only")
    group.add_argument("--parse", action="store_true", help="lex and parse only")
    group.add_argument(
        "--codegen", action="store_true", help="lex, parse, and generate assembly only"
    )
    parser.add_argument("-S", action="store_true", help="emit assembly")
    parser.add_argument("file")

    args = parser.parse_args()

    lex_only: bool = args.lex
    parse_only: bool = args.parse
    codegen_only: bool = args.codegen

    (input_base, _) = os.path.splitext(args.file)
    input_path = args.file
    preprocess_path = input_base + ".i"
    assembly_path = input_base + ".s"
    output_path = input_base

    cleanup = _make_cleanup([preprocess_path, assembly_path, output_path])

    try:
        # pre-process source file
        subprocess.run(
            ["gcc", "-E", "-P", input_path, "-o", preprocess_path], check=True
        )

        # compile pre-processed source file

        # read source & perform lexing
        with open(preprocess_path, "r", encoding="ascii") as preprocess_file:
            source = preprocess_file.read()

        tokens = lex(source)
        pp(tokens)
        if lex_only:
            cleanup()
            sys.exit(0)

        # TODO: perform parsing
        ast = parse(tokens)
        pp(ast)
        if parse_only:
            cleanup()
            sys.exit(0)

        # TODO: perform codegen
        # codegen()
        if codegen_only:
            cleanup()
            sys.exit(0)

        # TODO: emit assembly
        open(assembly_path, "w", encoding="ascii").close()
        os.remove(preprocess_path)

        # assemble and link assembly file
        subprocess.run(["gcc", assembly_path, "-o", output_path], check=True)
        os.remove(assembly_path)

    except Exception:
        cleanup()
        raise


if __name__ == "__main__":
    main()
