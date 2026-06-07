import os
import glob

for path in glob.glob('c:/Users/sametbtry/Desktop/flash-card-pwa/backend/**/*.py', recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    if 'from ' in content:
        content = content.replace('from ', 'from ')
        modified = True
    
    if path.endswith('main.py'):
        if 'from .database' in content:
            content = content.replace('from .database', 'from database')
            modified = True
        if 'from .routers' in content:
            content = content.replace('from .routers', 'from routers')
            modified = True
            
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {path}")
