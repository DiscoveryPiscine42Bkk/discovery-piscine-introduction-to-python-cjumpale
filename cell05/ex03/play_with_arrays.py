original = [2, 8, 9, 48, 8, 22, -12, 2]

new = set()
for num in original:
    if num > 5:
        new.add(num + 2)

print(original)
print(new)
