from sympy import sympify
from colorama import Fore
import os

def solve_equation(equation):
    try:
        # Using sympify for safe expression evaluation
        result = sympify(equation)
        return result.evalf()  # Evaluate the result as a floating-point number
    except Exception as e:
        return f"{Fore.RED}ERROR:{Fore.RESET} {e}"

while 1:
    equation = input(f'{Fore.GREEN}Type ++ to exit>>{Fore.RESET} ')
    if equation.lower() == '++':
        break
    result = solve_equation(equation)
    print(result)
    
