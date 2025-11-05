import sys

if len(sys.argv) != 2:
    print("none")
else:
    text = sys.argv[1]
    result = ""

    for char in text:
        if char == "z":
            result += "z"

    if result == "":
        print("none")
    else:
        print(result)
