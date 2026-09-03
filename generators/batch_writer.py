import json, base64, os

def write_mapping(data):
    for path, b64_val in data.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(b64_val))
        print(f'Successfully wrote {path}')
