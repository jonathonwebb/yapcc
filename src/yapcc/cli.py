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

import argparse
import contextlib
import os
import subprocess
import sys

def cleanup(files):
    for f in files:
        with contextlib.suppress(FileNotFoundError):
            os.remove(f)

def lex():
    pass

def parse():
    pass

def codegen():
    pass

def main():
    parser = argparse.ArgumentParser(description='Yet Another Python C Compiler')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--lex', action='store_true', help='lex only')
    group.add_argument('--parse', action='store_true', help='lex and parse only')
    group.add_argument('--codegen', action='store_true', help='lex, parse, and generate assembly only')
    parser.add_argument('-S', action='store_true', help='emit assembly')
    parser.add_argument('file')

    args = parser.parse_args()

    lex_only = args.lex
    parse_only = args.parse
    codegen_only = args.codegen

    (file_base, _) = os.path.splitext(args.file)
    preprocess_file = file_base + '.i'
    assembly_file = file_base + '.s'
    output_file = file_base

    all_files = [preprocess_file, assembly_file, output_file]

    try:
        # pre-process source file
        subprocess.run(['gcc', '-E', '-P', args.file, '-o', preprocess_file], check=True)

        # compile pre-processed source file

        # perform lexing
        lex()
        if lex_only:
            cleanup(all_files)
            sys.exit(0)

        # perform parsing
        parse()
        if parse_only:
            cleanup(all_files)
            sys.exit(0)
        
        # perform codegen
        codegen()
        if codegen_only:
            cleanup(all_files)
            sys.exit(0)

        # emit assembly
        open(assembly_file, 'w').close() # TODO: this step is stubbed
        os.remove(preprocess_file)

        # assemble and link assembly file
        subprocess.run(['gcc', assembly_file, '-o', output_file], check=True)
        os.remove(assembly_file)

    except Exception as err:
        cleanup([preprocess_file, assembly_file, output_file])
        raise

if __name__ == '__main__':
    main()