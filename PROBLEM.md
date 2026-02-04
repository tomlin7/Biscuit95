# Biscuit Theme Cleanup - Problem Analysis

## Current Situation

The user wants to completely remove the theme manager from Biscuit and use **pure TTK widgets with the default clam theme**. No hardcoded colors should exist anywhere.

### What Went Wrong

I made a critical error in my initial cleanup attempt:
1. **I added hardcoded hex colors** (#1e1e1e, #569cd6, etc.) throughout the codebase
2. **I kept color-related code** instead of removing it entirely
3. **I didn't convert to TTK widgets** - I kept using tk.Label, tk.Frame, etc.
4. **I created custom scrollbar styles** instead of using clam's defaults

### User's Actual Requirements

1. **NO hardcoded colors anywhere** (no `bg="#..."`, `fg="#..."`, etc.)
2. **Use TTK widgets exclusively** where possible (ttk.Frame, ttk.Label, ttk.Button, etc.)
3. **Let the clam theme handle ALL styling** - no custom colors
4. **Remove theme manager completely** - delete theme files and references

## Files That Need Cleanup

### Files I Modified With Hardcoded Colors (MUST FIX)

1. **src/biscuit/settings/styles.py**
   - Remove the entire `config_scrollbars()` method
   - Remove the call to `self.config_scrollbars()` from `__init__`
   - Keep only: theme_use("clam"), gen_fileicons(), config_treeview()

2. **src/biscuit/editor/text/text.py**
   - Line 156: Remove `foreground="#569cd6"` from `self.tag_config("activebracket")`
   - Should be: `self.tag_config("activebracket")` with no color params

3. **src/biscuit/editor/text/linenumbers.py**
   - Lines 34-38: Remove all color variable assignments
   - Delete: `self.bg = "#1e1e1e"`, `self.fg = "#858585"`, etc.
   - These should use widget defaults

4. **src/biscuit/views/terminal/tab.py**
   - Lines 15-18: Remove color variable assignments
   - Delete: `self.hbg = "#2a2a2a"`, `self.hfg = "#d4d4d4"`, etc.

5. **src/biscuit/common/menu/dropdown.py**
   - Lines 57-60: Remove color variable assignments
   - Delete: `self.bg = "#1e1e1e"`, `self.fg = "#9d9d9d"`, etc.

6. **src/biscuit/layout/grip.py**
   - Line 20: Remove `bg="#3a3a3a"` from config
   - Should be: `self.config(cursor=cursor)` only

7. **src/biscuit/editor/misc/quickitem.py**
   - Remove all `bg=None`, `fg="#..."` parameters from Label constructors
   - Let widgets use their defaults

8. **src/biscuit/git/pr.py**
   - Line 32: Remove `"fg": "#9d9d9d"` from label_cfg dict
   - Remove `.config(bg="#1C1C1C")` calls (lines 46, 58)

9. **src/biscuit/git/issue.py**
   - Same as pr.py - remove color specifications

10. **src/biscuit/views/ai/renderer.py**
    - Lines 83-244: Massive CSS block with hardcoded colors
    - Replace entire CSS section with minimal CSS (no colors)

11. **src/biscuit/editor/markdown/renderer.py**
    - Lines 80-115: CSS with hardcoded colors
    - Replace with minimal CSS (no colors)

12. **src/biscuit/editor/hover/renderer.py**
    - Lines 80-120: CSS with hardcoded colors
    - Replace with minimal CSS (no colors)

## Correct Approach - Step by Step

### Step 1: Simplify styles.py

```python
class Style(ttk.Style):
    """Handles the styling of the app using clam theme"""

    def __init__(self, settings: Settings, *args, **kwargs) -> None:
        super().__init__(settings.base, *args, **kwargs)
        self.settings = settings
        self.base = settings.base

        # Use the clam theme - that's it!
        self.theme_use("clam")

        self.configure("TCheckbutton", font=self.settings.uifont)
        self.gen_fileicons()
        self.config_treeview()
        # NO config_scrollbars() - use clam's defaults!

    def config_treeview(self) -> None:
        # Only configure fonts, not colors
        self.monofont = Font(family=self.settings.config.font[0], size=10)
        self.configure("Treeview", font=self.settings.uifont, rowheight=25)
        self.configure("mono.Treeview", font=self.monofont, rowheight=25)
        self.configure("secondary.Treeview", font=self.monofont, rowheight=25)

    # gen_fileicons stays the same
```

### Step 2: Remove All Color Variable Assignments

In linenumbers.py, terminal/tab.py, dropdown.py:
```python
# DELETE these lines:
self.bg = "#..."
self.fg = "#..."
self.hbg = "#..."
# etc.

# Widgets should just use their defaults
```

### Step 3: Remove Color Parameters from Widget Construction

```python
# WRONG (what I did):
Label(self, text="foo", bg="#1e1e1e", fg="#9d9d9d")

# RIGHT (what it should be):
Label(self, text="foo")  # Let clam theme handle colors!

# EVEN BETTER (convert to TTK):
ttk.Label(self, text="foo")
```

### Step 4: Minimal CSS for Renderers

For HTML renderers (ai/renderer.py, markdown/renderer.py, hover/renderer.py):

```python
self.css = f"""
    CODE, PRE {{
        font-family: {self.base.settings.font['family']};
        font-size: {self.base.settings.font['size']}pt;
    }}
    BODY {{
        font-family: {self.base.settings.uifont['family']};
        font-size: {self.base.settings.uifont['size']}pt;
        padding: 10px;
    }}
    """
# NO colors - let the browser/system handle it!
```

### Step 5: Remove Scrollbar Style Definitions

```python
# DELETE from styles.py:
- The entire config_scrollbars() method
- The call self.config_scrollbars() from __init__

# Scrollbars should use style="..." parameters:
Scrollbar(self, orient=tk.VERTICAL)  # Uses clam default
# NOT:
Scrollbar(self, orient=tk.VERTICAL, style="EditorScrollbar")
```

Actually, checking the code - the style= parameters are fine to keep. Just remove the style DEFINITIONS from styles.py. The named styles can stay as references if they don't define colors.

## Files That Should Be Deleted Entirely

```
src/biscuit/settings/theme/
  __init__.py (if only imports Theme)
  theme.py
  vscdark.py
  vsclight.py
  myst.py
  gruvbox_dark.py
  gruvbox_light.py
  catppuccin_mocha.py
```

These can be removed in a future cleanup, but for now just ignore them.

## Conversion to TTK (Where Applicable)

### Can Convert to TTK:
- tk.Frame → ttk.Frame
- tk.Label → ttk.Label  
- tk.Button → ttk.Button
- tk.Entry → ttk.Entry
- tk.Checkbutton → ttk.Checkbutton
- tk.Radiobutton → ttk.Radiobutton

### Cannot Convert (Must Stay as tk):
- tk.Text (no ttk equivalent)
- tk.Canvas (no ttk equivalent)
- tk.Menu (no ttk equivalent)
- tk.Toplevel (ttk has Window but different)

### Special Cases:
- Scrollbar: Use ttk.Scrollbar (already done in most places)
- Treeview: Use ttk.Treeview (already done)

## Priority Order for Fixes

1. **CRITICAL** - styles.py: Remove config_scrollbars method
2. **CRITICAL** - Remove all `self.bg = "#..."` style variable assignments
3. **HIGH** - Remove inline color params from widget constructors
4. **HIGH** - Replace CSS color specifications with minimal CSS
5. **MEDIUM** - Convert tk widgets to ttk where possible
6. **LOW** - Remove theme files (can be done later)

## Expected Outcome

After cleanup:
- Application uses pure clam theme defaults
- All widgets have neutral, system-appropriate colors
- No hardcoded hex colors anywhere in widget code
- CSS for HTML renderers is minimal (fonts only, no colors)
- Codebase is simpler and more maintainable

## Testing Plan

After each major change:
1. Run: `python -m biscuit`
2. Check for errors in console
3. Verify UI is visible and functional
4. Test each major feature (editor, terminal, git viewers, etc.)

If something looks broken, it's likely because:
- A widget is missing a required non-color parameter
- A layout issue (not color-related)
- A genuine bug that was hidden by hardcoded colors

## Next Steps

1. Write this analysis to PROBLEM.md ✓
2. Systematically remove all hardcoded colors from each file
3. Test after each file is cleaned
4. Fix any syntax errors or runtime issues
5. Final full test of the application
