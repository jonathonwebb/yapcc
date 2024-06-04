# pcc (Python C Compiler)

A Python implementation of the book [`Writing a C Compiler`](https://nostarch.com/writing-c-compiler) by Nora Sandler.

```
usage: pcc [-h] [--lex | --parse | --codegen] [-S] file

Python C Compiler

positional arguments:
  file

options:
  -h, --help  show this help message and exit
  --lex       lex only
  --parse     lex and parse only
  --codegen   lex, parse, and generate assembly only
  -S          emit assembly file
```
