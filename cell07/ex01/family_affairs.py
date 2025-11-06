def find_the_jumpalee(family):
    jumpalee = filter(lambda name: family[name] == "jumpalee", family.keys())
    return list(jumpalee)

jumpalee_family = {
    "chutiphon": "jumpalee",
    "vin": "diesel",
    "christian": "jumpalee",
    "lionel": "messi",
    "sam": "jumpalee"
}

print(find_the_jumpalee(jumpalee_family))
