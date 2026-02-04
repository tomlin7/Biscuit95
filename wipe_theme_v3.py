import os
import re

def wipe_theme(directory):
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
                    # 1. Handle assignments: var = self.base.theme.something
                    if '=' in line and 'theme' in line:
                        parts = line.split('=')
                        if 'theme' in parts[1] and not '(' in parts[1]:
                            lhs = parts[0]
                            num_vars = len(lhs.split(','))
                            if num_vars > 1:
                                line = lhs + '= ' + ', '.join(['None']*num_vars) + '\n'
                            else:
                                line = lhs + '= None\n'

                    # 2. Keyword arguments
                    # This is complex because they can be multi-line. 
                    # For now, let's target common ones.
                    keywords = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
                                'highlightbackground', 'highlightforeground', 'highlightcolor', 'selectbackground', 
                                'selectforeground', 'insertbackground', 'underlinefg']
                    
                    for kw in keywords:
                        # kw=self.base.theme.something
                        line = re.sub(r',\s*' + kw + r'=(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', line)
                        line = re.sub(kw + r'=(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+\s*,?\s*', '', line)

                    # 3. Double stars
                    line = re.sub(r',\s*\*\*self\.base\.theme\.[\w.]+', '', line)
                    line = re.sub(r'\*\*self\.base\.theme\.[\w.]+\s*,?\s*', '', line)
                    line = re.sub(r'\s*\*\*self\.base\.theme\.[\w.]+', '', line)

                    # 4. Clean up broken bits from previous runs
                    line = re.sub(r'pass\(\)', 'None', line)
                    line = re.sub(r'self\.\s*$', '', line.strip()) + '\n'
                    if line.strip() == 'self.': line = ''
                    if line.strip() == 'self.h': line = ''
                    
                    # 5. Fix commas
                    line = re.sub(r',\s*,', ',', line)
                    line = re.sub(r'\(\s*,', '(', line)
                    line = re.sub(r',\s*\)', ')', line)
                    
                    if line.strip():
                        new_lines.append(line)

                if new_lines != lines:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    wipe_theme('src')
