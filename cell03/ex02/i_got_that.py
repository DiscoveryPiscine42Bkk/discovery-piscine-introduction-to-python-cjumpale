while True:
    user = input("What you gotta say? : " if 'user' not in locals() else "I got that! Anything else? : ")
    if user == "STOP":
        break