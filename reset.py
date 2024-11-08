import json
with open("Bolao\\Exemplo.json", "r") as file:
    db = json.load(file)

with open("Bolao\\fds.json", "w") as file:
    json.dump(db, file, indent=4)

