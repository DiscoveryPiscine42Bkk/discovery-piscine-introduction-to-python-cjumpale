try:
    number = float(input(" "))
    if number < 0:
        print("This number is negative.")
    elif number > 0:
        print("This number is positive.")
    else:
        print("This number is both negative and positive.")
        
except ValueError:
    print("Invalid input: Please enter a valid number.")