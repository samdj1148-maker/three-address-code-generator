# Three Address Code Generator
# College Mini Project - Implements TAC generation in Python
# SDG 9: Industry, Innovation and Infrastructure

import re
from typing import List, Tuple

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.tac_code = []
    
    def new_temp(self) -> str:
        """Generate a new temporary variable"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label"""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def emit(self, code: str):
        """Add a TAC instruction"""
        self.tac_code.append(code)
    
    def parse_expression(self, expr: str) -> str:
        """Parse and generate TAC for expressions"""
        expr = expr.strip()
        
        # Handle parentheses
        if '(' in expr:
            return self.handle_parentheses(expr)
        
        # Handle operators with precedence
        for op in ['||', '&&']:
            if op in expr:
                return self.handle_binary_op(expr, op)
        
        for op in ['==', '!=', '<=', '>=', '<', '>']:
            if op in expr:
                return self.handle_binary_op(expr, op)
        
        for op in ['+', '-']:
            if op in expr and not expr.startswith(op):
                parts = expr.rsplit(op, 1)
                if len(parts) == 2 and parts[0].strip():
                    return self.handle_binary_op(expr, op)
        
        for op in ['*', '/', '%']:
            if op in expr:
                return self.handle_binary_op(expr, op)
        
        # If no operator found, return as is (variable or constant)
        return expr
    
    def handle_parentheses(self, expr: str) -> str:
        """Handle expressions with parentheses"""
        while '(' in expr:
            start = expr.rfind('(')
            end = expr.find(')', start)
            inner = expr[start+1:end]
            temp = self.parse_expression(inner)
            expr = expr[:start] + temp + expr[end+1:]
        return self.parse_expression(expr)
    
    def handle_binary_op(self, expr: str, op: str) -> str:
        """Handle binary operations"""
        parts = expr.rsplit(op, 1)
        if len(parts) != 2:
            return expr
        
        left = self.parse_expression(parts[0].strip())
        right = self.parse_expression(parts[1].strip())
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {op} {right}")
        return temp
    
    def generate_assignment(self, stmt: str):
        """Generate TAC for assignment statements"""
        match = re.match(r'(\w+)\s*=\s*(.+)', stmt)
        if match:
            var = match.group(1)
            expr = match.group(2)
            result = self.parse_expression(expr)
            self.emit(f"{var} = {result}")
    
    def generate_if(self, condition: str, true_block: List[str], false_block: List[str] = None):
        """Generate TAC for if-else statements"""
        cond_result = self.parse_expression(condition)
        label_false = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"if {cond_result} goto {label_false}")
        
        # True block
        for stmt in true_block:
            self.process_statement(stmt)
        
        if false_block:
            self.emit(f"goto {label_end}")
        
        self.emit(f"{label_false}:")
        
        # False block
        if false_block:
            for stmt in false_block:
                self.process_statement(stmt)
            self.emit(f"{label_end}:")
    
    def generate_while(self, condition: str, body: List[str]):
        """Generate TAC for while loops"""
        label_begin = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"{label_begin}:")
        cond_result = self.parse_expression(condition)
        self.emit(f"ifFalse {cond_result} goto {label_end}")
        
        for stmt in body:
            self.process_statement(stmt)
        
        self.emit(f"goto {label_begin}")
        self.emit(f"{label_end}:")
    
    def generate_for(self, init: str, condition: str, update: str, body: List[str]):
        """Generate TAC for for loops"""
        # Initialize
        self.process_statement(init)
        
        label_begin = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"{label_begin}:")
        cond_result = self.parse_expression(condition)
        self.emit(f"ifFalse {cond_result} goto {label_end}")
        
        for stmt in body:
            self.process_statement(stmt)
        
        self.process_statement(update)
        self.emit(f"goto {label_begin}")
        self.emit(f"{label_end}:")
    
    def process_statement(self, stmt: str):
        """Process a single statement"""
        stmt = stmt.strip()
        if not stmt or stmt.startswith('//'):
            return
        
        if '=' in stmt and not any(op in stmt.split('=')[0] for op in ['==', '!=', '<=', '>=']):
            self.generate_assignment(stmt)
    
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
        with open('test_input.txt', 'r') as f:
            input_code = f.readlines()
    except FileNotFoundError:
        print("Error: test_input.txt not found!")
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

if __name__ == "__main__":
    main()
