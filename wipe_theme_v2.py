import os
import re

def wipe_theme(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue
                
                initial_content = content

                # 1. Remove assignments: theme = ...
                content = re.sub(r'theme\s*=\s*(self\.base\.|self\.)theme', '# theme removed', content)
                content = re.sub(r't\s*=\s*(self\.base\.|self\.)theme', '# theme removed', content)

                # 2. Remove keyword arguments using theme or t
                # Matches: bg=theme.something, foreground=t.something, etc.
                patterns = [
                    r'bg\s*=\s*(?:theme|t)\.[\w.]+',
                    r'fg\s*=\s*(?:theme|t)\.[\w.]+',
                    r'background\s*=\s*(?:theme|t)\.[\w.]+',
                    r'foreground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'activebackground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'activeforeground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'highlightbackground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'highlightforeground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'highlightcolor\s*=\s*(?:theme|t)\.[\w.]+',
                    r'selectbackground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'selectforeground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'inactiveselectbackground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'insertbackground\s*=\s*(?:theme|t)\.[\w.]+',
                    r'underlinefg\s*=\s*(?:theme|t)\.[\w.]+',
                ]
                
                for p in patterns:
                    # Remove the pattern and optional surrounding commas
                    content = re.sub(r',\s*' + p, '', content)
                    content = re.sub(p + r'\s*,\s*', '', content)
                    content = re.sub(p, '', content)

                # 3. Handle self.base.theme usage directly in keyword args
                patterns_base = [
                    r'bg\s*=\s*self\.base\.theme\.[\w.]+',
                    r'fg\s*=\s*self\.base\.theme\.[\w.]+',
                    r'background\s*=\s*self\.base\.theme\.[\w.]+',
                    r'foreground\s*=\s*self\.base\.theme\.[\w.]+',
                    r'highlightbackground\s*=\s*self\.base\.theme\.[\w.]+',
                ]
                for p in patterns_base:
                    content = re.sub(r',\s*' + p, '', content)
                    content = re.sub(p + r'\s*,\s*', '', content)
                    content = re.sub(p, '', content)

                # 4. Clean up various theme-dependent configurations
                content = re.sub(r'\*\*self\.base\.theme\.[\w.]+', '', content)
                content = re.sub(r'\*\*theme\.[\w.]+', '', content)

                # 5. Fix any double commas or empty calls left behind
                content = re.sub(r',\s*,', ',', content)
                content = re.sub(r'\(\s*,', '(', content)
                content = re.sub(r',\s*\)', ')', content)
                content = re.sub(r'# theme removed\s*\n\s*', '', content)

                if content != initial_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    wipe_theme('src')
