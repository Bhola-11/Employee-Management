# WorkSphere Phase 1 Compiler
import os

def write_tpl(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Generated: {path}')

