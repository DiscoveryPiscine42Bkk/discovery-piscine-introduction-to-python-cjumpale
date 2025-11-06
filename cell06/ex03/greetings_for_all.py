def greetings(name="noble stranger"):
    if isinstance(name, str):
        print(f"Hello, {name}.")
    else:
        print("Error! It was not a name.")

greetings('Chutiphon')
greetings('Jumpalee')
greetings()
greetings(42)
