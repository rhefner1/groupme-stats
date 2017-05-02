import json

with open('data/output.json') as f:
    name_changes = json.load(f)

for names in name_changes.values():
    print ' -> '.join(names)