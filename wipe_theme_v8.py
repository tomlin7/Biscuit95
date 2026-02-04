import os
import re

def wipe_theme(directory):
    keywords = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
                'highlightbackground', 'highlightforeground', 'highlightcolor', 'selectbackground', 
                'selectforeground', 'insertbackground', 'underlinefg', 'buttonbackground',
                'highlightthickness', 'bd', 'relief', 'fill', 'outline', 'border', 'inactiveselectbackground',
                'activebracket', 'hover', 'currentline', 'currentword', 'foundcurrent', 'found']
    
    kw_theme_pattern = re.compile(
        r'(,\s*)?(' + '|'.join(keywords) + r')\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+(\s*,)?'
    )

    def kw_replacer(match):
        pre = match.group(1)
        post = match.group(3)
        if pre and ',' in pre and post:
            return ','
        return ''

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
                    # 1. State assignments
                    if re.search(r'^[ \t]+self\.[\w.]+\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', line):
                        line = re.sub(r'=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '= None', line)
                    
                    # 2. Keyword arguments
                    line = kw_theme_pattern.sub(kw_replacer, line)

                    # 3. Double star unpacks
                    line = re.sub(r'(,\s*)?\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+(\s*,)?', kw_replacer, line)

                    # 4. Clean up
                    line = re.sub(r',\s*,', ',', line)
                    line = re.sub(r'\(\s*,', '(', line)
                    line = re.sub(r',\s*\)', ')', line)
                    line = re.sub(r'\(,\)', '()', line)
                    
                    if re.search(r'^[ \t]*(?:theme|t)\s*=\s*(?:self\.base\.|self\.)?theme\s*$', line):
                         continue
                    
                    # Only add line if it's not just whitespace and was originally something else
                    if line.strip() or not line.strip(): # keep original empty lines
                         new_lines.append(line)

                if new_lines != lines:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    wipe_theme('src')
