try:
    number = float(input("Give me a number: "))
    
    if number.is_integer():
        print("This number is an integer.")
    
    else:
        print("This number is a decimal.")

except ValueError:
    print("Invalid input: Please enter a valid number.")
