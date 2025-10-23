# Three Address Code (TAC) Generator

## College Mini Project
**SDG 9: Industry, Innovation and Infrastructure**

## Overview
This project implements a Three Address Code (TAC) Generator in Python. TAC is an intermediate code representation used in compilers, where each instruction contains at most one operator in addition to assignment. This makes it easier for compiler optimization and code generation phases.

## Features
- ✅ Parses and converts high-level expressions into Three Address Code
- ✅ Handles arithmetic operations (+, -, *, /, %)
- ✅ Supports parenthesized expressions
- ✅ Generates temporary variables automatically
- ✅ Processes multiple statements from input file
- ✅ Clean and readable output format

## Project Structure
```
three-address-code-generator/
├── README.md           # Project documentation
├── main.py            # Main TAC generator implementation
├── requirements.txt   # Project dependencies
└── test_input.txt     # Sample input code for testing
```

## Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses Python standard library)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/samdj1148-maker/three-address-code-generator.git
cd three-address-code-generator
```

2. (Optional) Install development dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Generator
```bash
python main.py
```

The program will:
1. Read input code from `test_input.txt`
2. Parse and convert expressions to TAC
3. Display both input and generated TAC output

### Input Format
Create or modify `test_input.txt` with simple assignment statements:
```
x = 5
y = 10
z = x + y * 2
result = (x + y) * (z - 3)
```

### Sample Output
```
Input Code:
--------------------------------------------------
x = 5
y = 10
z = x + y * 2
result = (x + y) * (z - 3)

Generated Three Address Code:
--------------------------------------------------
x = 5
y = 10
t0 = y * 2
t1 = x + t0
z = t1
t2 = x + y
t3 = z - 3
t4 = t2 * t3
result = t4

==================================================
TAC Generation Complete!
Total Instructions: 9
==================================================
```

## How It Works

### TAC Generation Process
1. **Expression Parsing**: Breaks down complex expressions into simpler operations
2. **Operator Precedence**: Respects standard mathematical operator precedence
3. **Temporary Variables**: Generates temporary variables (t0, t1, t2, ...) for intermediate results
4. **Sequential Instructions**: Converts nested operations into sequential three-address instructions

### Example Transformation
**Input:** `result = (a + b) * (c - d)`

**Generated TAC:**
```
t0 = a + b
t1 = c - d
t2 = t0 * t1
result = t2
```

## Key Components

### TACGenerator Class
- `new_temp()`: Generates unique temporary variables
- `parse_expression()`: Parses and converts expressions
- `handle_binary_op()`: Processes binary operations
- `handle_parentheses()`: Handles nested parenthesized expressions
- `generate_assignment()`: Converts assignment statements to TAC
- `emit()`: Adds instructions to output

## Sustainable Development Goal (SDG)

### SDG 9: Industry, Innovation and Infrastructure
This project contributes to SDG 9 by:
- 🔧 **Innovation in Compiler Technology**: Demonstrates fundamental compiler design principles
- 📚 **Educational Infrastructure**: Provides learning resource for compiler construction
- 💡 **Technology Advancement**: Implements intermediate code generation techniques
- 🌱 **Knowledge Building**: Supports innovation in software engineering education

## Technical Concepts

### What is Three Address Code?
Three Address Code is an intermediate representation where:
- Each instruction has at most three operands
- Complex expressions are broken into simple operations
- Makes optimization and code generation easier
- Acts as bridge between high-level code and machine code

### Benefits of TAC
- ✅ Easier to optimize
- ✅ Machine-independent
- ✅ Explicit temporary values
- ✅ Simplified control flow analysis

## Testing

Modify `test_input.txt` with your own expressions and run:
```bash
python main.py
```

Try different expressions:
- Arithmetic: `x = a + b - c * d / e`
- Parentheses: `y = (a + b) * (c - d)`
- Complex: `z = ((a + b) * c) - (d / e)`

## Future Enhancements
- [ ] Support for if-else statements
- [ ] Loop constructs (for, while)
- [ ] Boolean operations
- [ ] Function calls
- [ ] Array indexing
- [ ] Optimization passes

## Contributing
This is a college mini project. Suggestions and improvements are welcome!

## License
Open source - free to use for educational purposes.

## Author
**College Mini Project**  
Implemented as part of compiler design coursework  
SDG 9: Industry, Innovation and Infrastructure

## Acknowledgments
- Compiler Design Principles
- Three Address Code Theory
- Python Programming Community

---

**Made with 💻 for learning compiler construction fundamentals**
