try:
    first_number = int(input("Give me the first number : "))
    second_number = int(input("Give me the second number : "))

    print("Thank you!")
    print(f"{first_number} + {second_number} = {first_number + second_number}")
    print(f"{first_number} - {second_number} = {first_number - second_number}")
    print(f"{first_number} / {second_number} = {first_number // second_number}")
    print(f"{first_number} * {second_number} = {first_number * second_number}")

except ValueError:
    print("Invalid input: Please enter a valid number.")