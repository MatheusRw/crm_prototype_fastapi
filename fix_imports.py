# fix_imports.py (deve estar na pasta raiz)
import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir from .import
        content = re.sub(r'from \.(\w+) import', r'from \1 import', content)
        content = re.sub(r'from \. import (\w+)', r'import \1', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Corrigido: {filepath}")
    except Exception as e:
        print(f"❌ Erro em {filepath}: {e}")

# Corrigir todos os arquivos Python na pasta app
app_dir = "app"
for filename in os.listdir(app_dir):
    if filename.endswith('.py'):
        filepath = os.path.join(app_dir, filename)
        fix_file(filepath)

print("🎉 Todas as importações corrigidas!")