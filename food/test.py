import os

EXCLUDE_DIRS = {'.venv', '__pycache__', '.git', 'migrations', '.idea', '.vscode'}
MAX_DEPTH = 2

def print_tree(base_path, prefix="", depth=0):
    if depth > MAX_DEPTH:
        return
    entries = sorted(
        [e for e in os.listdir(base_path) if e not in EXCLUDE_DIRS],
        key=lambda s: s.lower()
    )
    for index, entry in enumerate(entries):
        path = os.path.join(base_path, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if index == len(entries) - 1 else "│   ")
            print_tree(path, new_prefix, depth + 1)

print_tree(".")