# Less Language Compiler

A minimalist programming language compiler built from scratch in Python. 
**Less is more** - simple syntax, powerful compiler concepts.

## Features
- ✅ Lexical analysis and tokenization
- ✅ Recursive descent parsing  
- ✅ Abstract Syntax Tree (AST) generation
- ✅ Arithmetic operations (+, -, *, /)
- ✅ Variable declarations and assignments
- ✅ Print statements

## Example
```less
let x = 5
let y = x + 3 * 2
print(y)  # Output: 11
print((x + y) * 2)  # Output: 32
less-compiler/
├── src/less/           # Compiler source code
├── examples/           # Usage examples
├── tests/              # Unit tests
└── docs/               # Documentation