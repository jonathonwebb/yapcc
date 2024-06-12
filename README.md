# yapcc

> Yet Another Python C Compiler [^1]

A Python implementation of the learning x86 C compiler from the book [`Writing a C Compiler`](https://nostarch.com/writing-c-compiler) by Nora Sandler.

```
usage: yapcc [-h] [--lex | --parse | --codegen] [-S] file

Yet Another Python C Compiler

positional arguments:
  file

options:
  -h, --help  show this help message and exit
  --lex       lex only
  --parse     lex and parse only
  --codegen   lex, parse, and generate assembly only
  -S          emit assembly
```

[^1]: not to be confused with:

    - `yacc`: Yet Another Compiler-Compiler
    - `pcc`: Portable C Compiler
