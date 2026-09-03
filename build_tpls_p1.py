# WorkSphere Phase 1 Templates Compiler
import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Generated: {path}')

print('Phase 1 templates builder initialized')
