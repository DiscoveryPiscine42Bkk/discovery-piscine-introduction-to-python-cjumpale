import math

try:
    number = float(input("Give me a number: "))
    rounded = math.ceil(number)
    print(rounded)
    
except ValueError:
    print("Invalid input: Please enter a valid number.")