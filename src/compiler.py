# ===== COMPILER.PY - COMPLETE FILE =====
from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LET = "LET"
    IDENTIFIER = "IDENTIFIER"
    ASSIGN = "ASSIGN"
    PRINT = "PRINT"
    EOF = "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def lex(source_code):
    tokens = []
    position = 0
    while position < len(source_code):
        char = source_code[position]
        if char.isspace():
            position += 1
            continue
        elif char.isdigit():
            start = position
            while position < len(source_code) and source_code[position].isdigit():
                position += 1
            number = source_code[start:position]
            tokens.append(Token(TokenType.NUMBER, int(number)))
        elif char.isalpha():
            start = position
            while position < len(source_code) and source_code[position].isalnum():
                position += 1
            word = source_code[start:position]
            if word == "let":
                tokens.append(Token(TokenType.LET, word))
            elif word == "print":
                tokens.append(Token(TokenType.PRINT, word))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, word))
        elif char == '+':
            tokens.append(Token(TokenType.PLUS, '+'))
            position += 1
        elif char == '-':
            tokens.append(Token(TokenType.MINUS, '-'))
            position += 1
        elif char == '*':
            tokens.append(Token(TokenType.MULTIPLY, '*'))
            position += 1
        elif char == '/':
            tokens.append(Token(TokenType.DIVIDE, '/'))
            position += 1
        elif char == '(':
            tokens.append(Token(TokenType.LPAREN, '('))
            position += 1
        elif char == ')':
            tokens.append(Token(TokenType.RPAREN, ')'))
            position += 1
        elif char == '=':
            tokens.append(Token(TokenType.ASSIGN, '='))
            position += 1
        else:
            raise Exception(f"Unknown character: {char}")
    tokens.append(Token(TokenType.EOF, None))
    return tokens

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOp({self.left}, '{self.op}', {self.right})"

class VariableDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"VariableDeclaration('{self.name}', {self.value})"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Variable('{self.name}')"

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"PrintStatement({self.expression})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token(TokenType.EOF, None)
    
    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.position += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token().type}")
    
    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements
    
    def parse_statement(self):
        token = self.current_token()
        if token.type == TokenType.LET:
            return self.parse_variable_declaration()
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()
        else:
            return self.parse_expression()
    
    def parse_variable_declaration(self):
        self.eat(TokenType.LET)
        var_name = self.current_token().value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        return VariableDeclaration(var_name, value)
    
    def parse_print_statement(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.parse_expression()
        self.eat(TokenType.RPAREN)
        return PrintStatement(expr)
    
    def parse_expression(self):
        left = self.parse_term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.eat(op_token.type)
            right = self.parse_term()
            left = BinaryOp(left, op_token.value, right)
        return left
    
    def parse_term(self):
        left = self.parse_factor()
        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token()
            self.eat(op_token.type)
            right = self.parse_factor()
            left = BinaryOp(left, op_token.value, right)
        return left
    
    def parse_factor(self):
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.IDENTIFIER:
            var_name = token.value
            self.eat(TokenType.IDENTIFIER)
            return Variable(var_name)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            raise Exception(f"Unexpected token: {token}")

class Interpreter:
    def __init__(self):
        self.variables = {}
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_Number(self, node):
        return node.value
    
    def visit_BinaryOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if node.op == '+': return left_val + right_val
        elif node.op == '-': return left_val - right_val
        elif node.op == '*': return left_val * right_val
        elif node.op == '/': return left_val / right_val
        else: raise Exception(f"Unknown operator: {node.op}")
    
    def visit_VariableDeclaration(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value
        return value
    
    def visit_Variable(self, node):
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise Exception(f"Variable '{node.name}' not defined")
    
    def visit_PrintStatement(self, node):
        value = self.visit(node.expression)
        print(value)
        return value

# Test
if __name__ == "__main__":
    code = "let x = 5\nlet y = x + 3\nprint(y)"
    lines = code.split('\n')
    interpreter = Interpreter()
    
    for line in lines:
        if line.strip():
            tokens = lex(line)
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter.visit(ast[0])
    
    print("Final variables:", interpreter.variables)
def quick_test():
    code = "let x = 5"
    tokens = lex(code)
    print("Input:", code)
    print("Tokens:", tokens)
    
    # Check each token
    for i, token in enumerate(tokens):
        print(f"Token {i}: {token.type} -> '{token.value}'")

quick_test()