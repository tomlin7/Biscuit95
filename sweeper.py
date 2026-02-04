import os
import re

def sweep_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files that are likely the theme engine itself if we want to be safe, 
    # but the user said sweep the repo.
    if 'src/biscuit/settings/theme/' in filepath.replace('\\', '/') and filepath.endswith('theme.py'):
        # Keep the Stub/Base classes but maybe remove specific theme files later.
        pass

    initial_content = content

    # 1. Remove thematic keyword arguments from calls (e.g. bg=self.base.theme.xxx)
    # Target: bg, fg, background, foreground, activebackground, etc.
    # regex: (optional comma) (space) (kw) = (base.theme chain) (optional comma)
    theme_ref = r'(?:self\.base\.|self\.|base\.|t\.|theme\.)?theme\.[\w.]+'
    
    # Remove kwargs in widget calls
    kwargs = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
              'highlightbackground', 'highlightforeground', 'selectbackground', 'selectforeground',
              'insertbackground', 'buttonbackground', 'underlinefg']
    
    for kw in kwargs:
        # Match kw=theme_ref, handles optional leading/trailing commas
        pattern = r',\s*' + kw + r'=' + theme_ref
        content = re.sub(pattern, '', content)
        pattern = kw + r'=' + theme_ref + r',\s*'
        content = re.sub(pattern, '', content)
        pattern = kw + r'=' + theme_ref
        content = re.sub(pattern, '', content)

    # 2. Remove unpacking of theme dicts
    # Target: **self.base.theme.xxx
    content = re.sub(r',\s*\*\*' + theme_ref, '', content)
    content = re.sub(r'\*\*' + theme_ref + r',\s*', '', content)
    content = re.sub(r'\*\*' + theme_ref, '', content)

    # 3. Handle assignments like self.bg = self.base.theme.xxx
    # We'll replace these with None if they are standalone assignments
    content = re.sub(r'([ \t]+[\w._]+)\s*=\s*' + theme_ref + r'[ \t]*$', r'\1 = None', content, flags=re.MULTILINE)

    # 4. Handle multiple assignments like self.bg, self.fg = self.base.theme.xxx.values()
    # Replace with self.bg, self.fg = None, None (or similar)
    # The previous failed regex produced: self.bg, self.fg, self.hbg, self.()
    # Let's fix that specifically first.
    content = re.sub(r'self\.bg, self\.fg, self\.hbg, self\.\(\)', 'self.bg = self.fg = self.hbg = self.hfg = None', content)
    
    # Generic multiple assignment fix
    def fix_multi_assign(match):
        vars_part = match.group(1)
        count = vars_part.count(',') + 1
        return vars_part + ' = ' + ', '.join(['None'] * count)

    content = re.sub(r'([ \t]+[\w._, ]+)\s*=\s*' + theme_ref + r'\.values\(\)', fix_multi_assign, content)

    # 5. Cleanup syntax remnants
    content = re.sub(r',\s*,', ',', content)
    content = re.sub(r'\(\s*,', '(', content)
    content = re.sub(r',\s*\)', ')', content)
    content = re.sub(r'\(\s*\)', '()', content)
    
    # 6. Specific cleanup for common remaining patterns
    content = re.sub(r'theme = self\.base\.theme', '', content)
    content = re.sub(r't = self\.base\.theme', '', content)

    if content != initial_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = r'c:\Users\BIT\Documents\github\biscuit90s\src'
    modified_count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                if sweep_file(path):
                    modified_count += 1
    print(f"Swept {modified_count} files.")

if __name__ == "__main__":
    main()
