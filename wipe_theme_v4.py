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
                    # 1. Assignments like self.bg = self.base.theme...
                    # Regex explanation: matches optional indentation, followed by variable(s), then '=', then theme reference
                    # Example match: "    self.bg = self.base.theme.views.sidebar.item.background"
                    if re.search(r'=\s*(self\.base\.|self\.|theme|t)\.?theme', line) and not '(' in line:
                        parts = line.split('=')
                        lhs = parts[0]
                        num_vars = len(lhs.split(','))
                        if num_vars > 1:
                            line = lhs + '= ' + ', '.join(['None']*num_vars) + '\n'
                        else:
                            line = lhs + '= None\n'
                    
                    # 2. Keyword arguments in calls
                    keywords = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
                                'highlightbackground', 'highlightforeground', 'highlightcolor', 'selectbackground', 
                                'selectforeground', 'insertbackground', 'underlinefg', 'buttonbackground',
                                'highlightthickness', 'bd', 'relief']
                    
                    for kw in keywords:
                        # Matches arguments using theme
                        line = re.sub(r',\s*' + kw + r'=(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', line)
                        line = re.sub(kw + r'=(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+\s*,?\s*', '', line)

                    # 3. Double star unpacks
                    line = re.sub(r',\s*\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', line)
                    line = re.sub(r'\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+\s*,?\s*', '', line)
                    line = re.sub(r'\s*\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', line)

                    # 4. Clean up commas and empty calls
                    line = re.sub(r',\s*,', ',', line)
                    line = re.sub(r'\(\s*,', '(', line)
                    line = re.sub(r',\s*\)', ')', line)

                    new_lines.append(line)

                if new_lines != lines:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    wipe_theme('src')
