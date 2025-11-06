def array_of_names(persons):
    full_names = []
    for first, last in persons.items():
        full_name = first.capitalize() + " " + last.capitalize()
        full_names.append(full_name)
    return full_names

persons = {
    "chutiphon": "jumpalee",
    "david": "beckham",
    "michael": "jackson",
    "steve": "jobs"
}

print(array_of_names(persons))
