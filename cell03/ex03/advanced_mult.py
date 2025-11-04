table = 0
while table <= 10:
    print(f"Table de {table}:", end=" ")
    
    i = 0
    while i <= 10:
        print(table * i, end=" ")
        i += 1

    print()
    table += 1