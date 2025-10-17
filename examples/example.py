# example.py - Demo of TinyLang Compiler
from compiler import lex, Parser, Interpreter

def run_example(code, description):
    print(f"\n{'='*50}")
    print(f"EXAMPLE: {description}")
    print(f"{'='*50}")
    print("Code:")
    print(code)
    print("\nOutput:")
    
    interpreter = Interpreter()
    lines = code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            try:
                tokens = lex(line)
                parser = Parser(tokens)
                ast = parser.parse()
                for node in ast:
                    interpreter.visit(node)
            except Exception as e:
                print(f"Error: {e}")

# Example 1: Basic Math
math_example = """
5 + 3 * 2
(10 + 5) / 3
8 - 4
"""

# Example 2: Variables
variable_example = """
let x = 10
let y = x + 5
let z = y * 2
print(z)
"""

# Example 3: Complex Expressions
complex_example = """
let a = 5
let b = 3
let result = (a + b) * 2 - 1
print(result)
"""

# Example 4: Multiple Operations
multi_example = """
let base = 10
let height = 5
let area = base * height / 2
print(area)
"""

if __name__ == "__main__":
    print(" TINYLANG COMPILER DEMO")
    print("Showing what the compiler can do:\n")
    
    run_example(math_example, "Basic Arithmetic Operations")
    run_example(variable_example, "Variable Declarations and Usage")
    run_example(complex_example, "Complex Expressions with Variables")
    run_example(multi_example, "Multiple Operations (Area Calculation)")
    
    print(f"\n{'='*50}")
    print(" All examples completed!")
    print("This demonstrates a working compiler with:")
    print(" Lexical Analysis (Tokenization)")
    print(" Syntactic Parsing (AST Generation)") 
    print("Expression Evaluation")
    print(" Variable Support")
    print(" Print Statements")
    print(f"{'='*50}") 