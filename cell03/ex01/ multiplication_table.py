try:
    number = int(input("Enter a number\n"))
    for i in range(13):
        print(f"{i} x {number} = {i * number}")

except ValueError:
    print("Invalid input: Please enter a valid number.")