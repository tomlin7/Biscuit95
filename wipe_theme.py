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

                # Remove theme-related imports if possible (tricky, so just leave them for now or be careful)

                # Aggressive regex replacements for arguments in calls
                # Pattern: matches , **self.base.theme... or **self.base.theme...
                content = re.sub(r',\s*\*\*self\.base\.theme\.[\w.]+', '', content)
                content = re.sub(r'\*\*self\.base\.theme\.[\w.]+\s*,?\s*', '', content)
                
                # List of common style attributes to strip if they use theme
                attrs = [
                    'background', 'foreground', 'activebackground', 'activeforeground', 
                    'highlightbackground', 'highlightforeground', 'selectbackground', 
                    'selectforeground', 'bg', 'fg', 'insertbackground', 'inactiveselectbackground',
                    'highlightcolor', 'underlinefg', 'buttonbackground'
                ]
                
                for attr in attrs:
                    # Case 1: , attr=self.base.theme.something
                    content = re.sub(r',\s*' + attr + r'\s*=\s*(?:self\.base\.|self\.)theme\.[\w.]+', '', content)
                    # Case 2: attr=self.base.theme.something, 
                    content = re.sub(attr + r'\s*=\s*(?:self\.base\.|self\.)theme\.[\w.]+\s*,\s*', '', content)
                    # Case 3: attr=self.base.theme.something (maybe last in call)
                    content = re.sub(attr + r'\s*=\s*(?:self\.base\.|self\.)theme\.[\w.]+', '', content)

                # Direct assignments
                # self.some_color = self.base.theme.some_color
                content = re.sub(r'(?:self\.)?[\w_]+\s*=\s*(?:self\.base\.|self\.)theme\.[\w.]+', 'pass', content)
                
                # Tags in text widgets
                # self.tag_config(..., background=self.base.theme...)
                # This is harder to do safely with one regex, but let's try
                # Actually most of it is already covered by the generic attr remover above.

                if content != initial_content:
                    # Clean up double commas or empty calls
                    content = re.sub(r'\(\s*,\s*', '(', content)
                    content = re.sub(r',\s*,\s*', ', ', content)
                    content = re.sub(r',\s*\)', ')', content)
                    content = re.sub(r'pass\s*\n\s*pass', 'pass', content)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    wipe_theme('src')
