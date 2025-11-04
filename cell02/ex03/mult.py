try:
    number1 = float(input())
    number2 = float(input())
    result = number1 * number2

    def clean(num):
        if num.is_integer():
            return int(num)
        return num

    print(f"{clean(number1)} x {clean(number2)} = {clean(result)}")

    if result > 0:
        print("This result is positive.")
    elif result < 0:
        print("This result is negative.")
    else:
        print("This result is both positive and negative.")

except ValueError:
    print("Invalid input: Please enter a valid number.")
