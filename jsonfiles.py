import json
def carregar_json(file_path, default):
    try:
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    except FileNotFoundError:
        return default

def salvar_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
