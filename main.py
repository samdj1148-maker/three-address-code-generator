# Three Address Code Generator
from typing import List
import re

class TACGenerator:
    def __init__(self):
        self.tac_code = []
        self.temp_counter = 1
        self.variables = set()
        
    def get_new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def is_operator(self, char):
        return char in ['+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|']
    
    def get_precedence(self, op):
        precedence = {
            '=': 0,
            '||': 1, '&&': 2,
            '==': 3, '!=': 3, '<': 3, '>': 3, '<=': 3, '>=': 3,
            '+': 4, '-': 4,
            '*': 5, '/': 5, '%': 5,
            '!': 6, 'unary-': 6, 'unary+': 6
        }
        return precedence.get(op, 0)
    
    def tokenize(self, expression):
        # Remove all whitespace
        expression = re.sub(r'\s+', '', expression)
        tokens = []
        i = 0
        
        while i < len(expression):
            if expression[i].isalnum() or expression[i] == '_':
                # Variable or number
                token = ''
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_' or expression[i] == '.'):
                    token += expression[i]
                    i += 1
                tokens.append(token)
            elif expression[i] in '+-*/()=<>!&|%':
                # Check for multi-character operators
                if i + 1 < len(expression):
                    two_char = expression[i:i+2]
                    if two_char in ['==', '!=', '<=', '>=', '&&', '||']:
                        tokens.append(two_char)
                        i += 2
                        continue
                tokens.append(expression[i])
                i += 1
            else:
                i += 1
                
        return tokens
    
    def infix_to_postfix(self, tokens):
        output = []
        operators = []
        
        for i, token in enumerate(tokens):
            if token.replace('.', '').replace('-', '').isdigit() or (token.isalpha() or '_' in token):
                output.append(token)
                if token.isalpha() or '_' in token:
                    self.variables.add(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators and operators[-1] == '(':
                    operators.pop()
            elif self.is_operator(token[0]) or token in ['==', '!=', '<=', '>=', '&&', '||']:
                # Handle unary operators
                if token in ['+', '-'] and (i == 0 or tokens[i-1] in ['('] or self.is_operator(tokens[i-1][0])):
                    token = f'unary{token}'
                
                while (operators and operators[-1] != '(' and 
                       self.get_precedence(operators[-1]) >= self.get_precedence(token)):
                    output.append(operators.pop())
                operators.append(token)
        
        while operators:
            output.append(operators.pop())
            
        return output
    
    def generate_tac_from_postfix(self, postfix, target_var=None):
        stack = []
        
        for token in postfix:
            if token.replace('.', '').replace('-', '').isdigit() or (token.isalpha() or '_' in token):
                stack.append(token)
            elif token.startswith('unary'):
                if stack:
                    operand = stack.pop()
                    temp = self.get_new_temp()
                    op = token[5:]  # Remove 'unary' prefix
                    self.tac_code.append(f"{temp} = {op}{operand}")
                    stack.append(temp)
            elif token in ['==', '!=', '<=', '>=', '&&', '||'] or self.is_operator(token[0]):
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    
                    if target_var and len(stack) == 0 and token == '=':
                        # This is the final assignment
                        self.tac_code.append(f"{target_var} = {left}")
                        stack.append(target_var)
                    else:
                        temp = self.get_new_temp()
                        self.tac_code.append(f"{temp} = {left} {token} {right}")
                        stack.append(temp)
        
        return stack[0] if stack else None
    
    def process_statement(self, statement):
        statement = statement.strip()
        if not statement or statement.startswith('#'):
            return
            
        # Check if it's an assignment
        if '=' in statement:
            parts = statement.split('=', 1)
            if len(parts) == 2:
                left_side = parts[0].strip()
                right_side = parts[1].strip()
                
                # Add the left side variable to our set
                self.variables.add(left_side)
                
                # Tokenize and convert the right side
                tokens = self.tokenize(right_side)
                if tokens:
                    postfix = self.infix_to_postfix(tokens)
                    self.generate_tac_from_postfix(postfix, left_side)
    
    def generate(self, statements: List[str]) -> List[str]:
        """Generate TAC for a list of statements"""
        for stmt in statements:
            self.process_statement(stmt)
        return self.tac_code

def main():
    print("=" * 50)
    print("Three Address Code (TAC) Generator")
    print("College Mini Project")
    print("SDG 9: Industry, Innovation and Infrastructure")
    print("=" * 50)
    print()
    
    # Read input from file
    try:
        with open('input.txt', 'r') as f:
            input_code = f.readlines()
    except FileNotFoundError:
        print("Error: input.txt not found!")
        print("\nUsing default example...\n")
        input_code = [
            "x = 5",
            "y = 10", 
            "z = x + y * 2",
            "result = (x + y) * (z - 3)"
        ]
    
    print("Input Code:")
    print("-" * 50)
    for line in input_code:
        print(line.strip())
    print()
    
    # Generate TAC
    generator = TACGenerator()
    tac_output = generator.generate(input_code)
    
    print("\nGenerated Three Address Code:")
    print("-" * 50)
    for instruction in tac_output:
        print(instruction)
    print()
    print("=" * 50)
    print("TAC Generation Complete!")
    print(f"Total Instructions: {len(tac_output)}")
    print("=" * 50)
    
    # Save output to file
    try:
        with open('output.txt', 'w') as f:
            f.write("Generated Three Address Code:\n")
            f.write("-" * 50 + "\n")
            for instruction in tac_output:
                f.write(instruction + "\n")
            f.write("\n")
            f.write("=" * 50 + "\n")
            f.write("TAC Generation Complete!\n")
            f.write(f"Total Instructions: {len(tac_output)}\n")
            f.write("=" * 50 + "\n")
        print("\nOutput saved to 'output.txt'")
    except Exception as e:
        print(f"\nError saving output to file: {e}")

if __name__ == "__main__":
    main()
