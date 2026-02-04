import os
import re

def wipe_theme(directory):
    # Keyword arguments to remove entirely
    keywords = ['bg', 'fg', 'background', 'foreground', 'activebackground', 'activeforeground', 
                'highlightbackground', 'highlightforeground', 'highlightcolor', 'selectbackground', 
                'selectforeground', 'insertbackground', 'underlinefg', 'buttonbackground',
                'highlightthickness', 'bd', 'relief', 'fill', 'outline', 'border', 'inactiveselectbackground',
                'activebracket', 'hover', 'currentline', 'currentword', 'foundcurrent', 'found']
    
    # Matches kw=theme_ref, with optional surrounding commas and spaces
    # Supports multi-line if needed by using [\s\S]*? but let's stick to single lines for safety first
    # and just run it multiple times if needed.
    kw_regex = r'(,\s*|^[ \t]*)(' + '|'.join(keywords) + r')\s*=\s*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+(\s*,)?'

    def remove_kw(match):
        pre_comma = match.group(1)
        post_comma = match.group(3)
        
        # If it was "meth(arg1, bg=theme.bg, arg2)"
        # group1 is ", " or similar
        # group3 is ","
        if pre_comma and pre_comma.strip() == ',' and post_comma:
            return ',' # keep the trailing comma for the next arg
        
        # If it was "meth(bg=theme.bg, arg2)"
        # group1 is "" (start of call/line)
        # group3 is ","
        if (not pre_comma or not ',' in pre_comma) and post_comma:
            return '' # remove kw and comma, next arg will handle its own prefix? No.
            # wait, if I have meth(bg=theme.bg, arg2), group1 is "" or spaces, group3 is ",".
            # I want to return "" so it becomes meth(arg2)
        
        return ''

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

                # 1. Assignments: self.bg = theme.xxx -> self.bg = None
                content = re.sub(r'([ \t]+[\w_, ]+\s*=\s*)(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+', r'\1None', content)

                # 2. Keyword arguments (single line)
                content = re.sub(kw_regex, remove_kw, content, flags=re.MULTILINE)

                # 3. Double star unpacks
                content = re.sub(r'(,\s*|^[ \t]*)\*\*(?:self\.base\.|self\.|theme|t)\.?theme\.[\w.]+(\s*,)?', remove_kw, content, flags=re.MULTILINE)

                # 4. Remove standalone theme assignments
                content = re.sub(r'^[ \t]*(?:theme|t)\s*=\s*(?:self\.base\.|self\.)?theme\s*$', '', content, flags=re.MULTILINE)
                
                # 5. Cleanup syntax remnants
                content = re.sub(r',\s*,', ',', content)
                content = re.sub(r'\(\s*,', '(', content)
                content = re.sub(r',\s*\)', ')', content)
                content = re.sub(r'\(,\)', '()', content)
                
                # Remove lines that became purely whitespace
                content = "\n".join([line for line in content.splitlines() if line.strip() or not line])

                if content != initial_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    wipe_theme('src')
