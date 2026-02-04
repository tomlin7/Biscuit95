#!/usr/bin/env python3
"""
Remove ALL hardcoded colors from Biscuit and use pure TTK with clam theme.
"""

import os
import re
from pathlib import Path


def remove_colors_from_styles_py(filepath):
    """Remove config_scrollbars method from styles.py"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove the config_scrollbars call
    content = re.sub(r"\s*self\.config_scrollbars\(\)", "", content)

    # Remove the entire config_scrollbars method
    pattern = r"\n    def config_scrollbars\(self\).*?(?=\n    def |\Z)"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Cleaned {filepath}")


def remove_color_variables(filepath):
    """Remove color variable assignments"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if re.search(
            r'self\.(bg|fg|hbg|hfg|bp_hover_color|bp_enabled_color|iconfg|iconbg|iconhfg|iconhbg)\s*=\s*"#',
            line,
        ):
            continue
        new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"✓ Cleaned {filepath}")


def remove_inline_color_params(filepath):
    """Remove all color parameters"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove all color parameters
    color_params = [
        "bg",
        "fg",
        "background",
        "foreground",
        "troughcolor",
        "arrowcolor",
        "activebackground",
        "activeforeground",
        "iconfg",
        "iconhfg",
    ]

    for param in color_params:
        content = re.sub(
            rf',?\s*{param}\s*=\s*["\']#[0-9a-fA-F]{{3,6}}["\'],?', "", content
        )
        content = re.sub(
            rf',?\s*{param}\s*=\s*["\'][^"\']*["\'],?\s*(?=#|\))', "", content
        )

    # Clean up config calls with only bg/fg
    content = re.sub(r"\.config\(bg=[^)]+\)", "", content)

    # Clean up syntax issues
    content = re.sub(r"\(\s*,", "(", content)
    content = re.sub(r",\s*,", ",", content)
    content = re.sub(r",\s*\)", ")", content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Cleaned {filepath}")


def minimal_css(filepath):
    """Replace CSS with minimal version without colors"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find CSS section and replace with minimal CSS
    css_minimal = '''f"""
            CODE, PRE {{
                font-family: {self.base.settings.font['family']};
                font-size: {self.base.settings.font['size']}pt;
            }}
            BODY {{
                font-family: {self.base.settings.uifont['family']};
                font-size: {self.base.settings.uifont['size']}pt;
            }}
            """'''

    # Replace CSS content
    content = re.sub(r'self\.css = f""".*?"""', css_minimal, content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Cleaned {filepath}")


# Run cleanup
src = Path("src/biscuit")

# Special files
remove_colors_from_styles_py(src / "settings/styles.py")
remove_color_variables(src / "editor/text/linenumbers.py")
remove_color_variables(src / "views/terminal/tab.py")
remove_color_variables(src / "common/menu/dropdown.py")

# Files with inline colors
for f in [
    "editor/text/text.py",
    "git/pr.py",
    "git/issue.py",
    "layout/grip.py",
    "editor/misc/quickitem.py",
]:
    remove_inline_color_params(src / f)

# Renderers - use minimal CSS
for f in [
    "views/ai/renderer.py",
    "editor/markdown/renderer.py",
    "editor/hover/renderer.py",
]:
    minimal_css(src / f)

print("\n✅ Cleanup complete!")
