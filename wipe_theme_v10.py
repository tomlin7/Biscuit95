import os
import re

def wipe_theme(directory):
    # Regex to catch theme references in various contexts
    # 1. **self.base.theme.xxx (with optional leading comma)
    unpack_pattern = re.compile(r',?\s*\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+')
    
    # 2. kw=self.base.theme.xxx (with optional leading comma)
    kw_pattern = re.compile(r'(,\s*)?[\w_]+\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+')
    
    # 3. Direct assignments: self.xxx = self.base.theme.yyy or theme = ...
    assign_pattern = re.compile(r'([ \t]+[\w._, ]+\s*=\s*)(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    continue
                
                new_lines = []
                for line in lines:
                    if 'theme' not in line:
                        new_lines.append(line)
                        continue
                    
                    # Skip the theme definition itself and the Theme stub usage in config.py
                    if 'class Theme' in line or 'from .theme import Theme' in line:
                        new_lines.append(line)
                        continue

                    original_line = line
                    
                    # 1. Unpacks: self.config(**theme.xxx) -> self.config()
                    line = unpack_pattern.sub('', line)
                    
                    # 2. Keyword args: self.config(bg=theme.xxx, fg=theme.yyy) -> self.config(bg=None, fg=None)
                    # Actually, let's just remove them.
                    line = kw_pattern.sub('', line)
                    
                    # 3. Assignments: self.bg = theme.xxx -> self.bg = None
                    line = assign_pattern.sub(r'\1None', line)
                    
                    # 4. Standalone theme assignments: theme = self.base.theme
                    if re.search(r'^[ \t]*(?:theme|t)\s*=\s*(?:self\.base\.|self\.)?theme\s*$', line):
                        continue

                    # Cleanup leftover commas and empty parentheses
                    line = re.sub(r',\s*,', ',', line)
                    line = re.sub(r'\(\s*,', '(', line)
                    line = re.sub(r',\s*\)', ')', line)
                    line = re.sub(r'\(\s*\)', '()', line)
                    
                    # If the line became just whitespace or "self.config()", let's see if we should keep it.
                    # Mostly, we can keep it for now to avoid breaking indentation if it was part of a block.
                    # But if it's JUST self.config(), it's better than nothing.
                    
                    new_lines.append(line)

                if new_lines != lines:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    wipe_theme('src')
