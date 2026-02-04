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

                # 1. Capture and replace assignments as standalone lines
                # We want to keep the variable but set it to None if it's used elsewhere, OR delete the whole line if it's safe.
                # Actually, setting it to None is safer to avoid UnboundLocalError.
                # Example: self.bg = self.base.theme.bg -> self.bg = None
                content = re.sub(r'([ \t]+[\w_, ]+\s*=\s*)(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', r'\1None', content)

                # 2. Keyword arguments in calls: kw=theme.xxx
                # We want to remove these completely.
                keywords = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
                            'highlightbackground', 'highlightforeground', 'highlightcolor', 'selectbackground', 
                            'selectforeground', 'insertbackground', 'underlinefg', 'buttonbackground',
                            'highlightthickness', 'bd', 'relief', 'fill', 'outline']
                
                for kw in keywords:
                    # Match comma followed by kw=theme...
                    content = re.sub(r',\s*' + kw + r'\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', content)
                    # Match kw=theme... followed by comma
                    content = re.sub(kw + r'\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+\s*,\s*', '', content)
                    # Match kw=theme... inside parentheses with no commas
                    content = re.sub(kw + r'\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', content)

                # 3. Double star unpacks
                content = re.sub(r',\s*\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', content)
                content = re.sub(r'\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+\s*,\s*', '', content)
                content = re.sub(r'\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', '', content)

                # 4. Clean up leftovers
                content = re.sub(r',\s*,', ',', content)
                content = re.sub(r'\(\s*,', '(', content)
                content = re.sub(r',\s*\)', ')', content)
                
                # 5. Extra cleanup for common patterns
                content = re.sub(r'theme\s*=\s*self\.base\.theme\n', '', content)
                content = re.sub(r't\s*=\s*self\.base\.theme\n', '', content)

                if content != initial_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    # Ensure theme.py is a stub first to prevent run-time errors if script misses something
    wipe_theme('src')
