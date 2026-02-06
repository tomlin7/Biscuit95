import tkinter as tk

from biscuit.common.ui import Button, Frame, ScrollableFrame
from biscuit.editor import BaseEditor

from .searchbar import Searchbar
from .section import Section


class SettingsEditor(BaseEditor):
    """Settings editor for changing the settings of the editor.

    - Add sections for different settings
    - Add items for each section to change the settings
    - Search through the settings to find the desired
    """

    name = "settings"

    def __init__(self, master, exists=False, editable=False, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # self.config(padx=100, pady=20)
        self.filename = "Settings"

        # TODO searchbar functionality not implemented yet
        # unpack the container and pack a new container for showing results
        self.search = Searchbar(self)
        self.search.pack(fill=tk.X)

        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = Frame(frame)  # , width=200, pady=20)
        self.tree.pack_propagate(False)
        self.tree.pack(fill=tk.Y, side=tk.LEFT, padx=(0, 1))

        self.sections = []
        self.container = ScrollableFrame(frame)
        self.container.content.config(padding=(50, 10))
        self.container.pack(fill=tk.BOTH, expand=True)

        self.add_sections()

    def add_sections(self):
        self.add_commonly_used()
        self.add_text_editor()
        self.add_clippy_config()
        self.add_ai_config()

    def add_commonly_used(self):
        """Add commonly used settings to the settings editor"""

        commonly_used = self.add_section(f"Commonly Used")

        commonly_used.add_dropdown("Color Theme", ("dark", "light"))
        commonly_used.add_intvalue("Font Size", 14)
        commonly_used.add_stringvalue("Font Family", "Consolas")
        commonly_used.add_intvalue("Tab Size", 4)

    def add_text_editor(self):
        """Add text editor settings to the settings editor"""

        commonly_used = self.add_section(f"Text Editor")
        commonly_used.add_checkbox("Auto Save", False)
        commonly_used.add_checkbox("Auto Closing Pairs", True)
        commonly_used.add_checkbox("Auto Closing Delete", True)
        commonly_used.add_checkbox("Auto Indent", True)
        commonly_used.add_checkbox("Auto Surround", True)
        commonly_used.add_checkbox("Word Wrap", False)

    def add_clippy_config(self):
        """Add Clippy configuration settings to the settings editor"""
        clippy = self.add_section(f"Clippy (BETA)")
        
        self.clippy_enabled_item = clippy.add_checkbox("Enable Clippy", self.base.config.clippy_enabled)
        
        tk.Label(clippy, text="Active Listeners", font=self.base.settings.uifont_bold, anchor=tk.W).pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.clippy_listeners_items = {}
        for listener in ["ast", "terminal", "git", "user_behavior"]:
            active = listener in self.base.config.clippy_listeners
            self.clippy_listeners_items[listener] = clippy.add_checkbox(f"  {listener.replace('_', ' ').title()}", active)
        
        from biscuit.common.ui import IconLabelButton, Icons
        IconLabelButton(clippy, "Apply Clippy Settings", Icons.SAVE, self.save_clippy_settings).pack(fill=tk.X, pady=10)

    def add_ai_config(self):
        """Add AI configuration settings to the settings editor"""
        import os
        import toml

        ai = self.add_section(f"AI Configuration")
        
        secrets_path = os.path.join(self.base.datadir, "secrets.toml")
        gemini_key = ""
        anthropic_key = ""
        
        try:
            if os.path.exists(secrets_path):
                with open(secrets_path, "r") as f:
                    secrets = toml.load(f)
                    gemini_key = secrets.get("GEMINI_API_KEY", "")
                    anthropic_key = secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            pass

        self.gemini_item = ai.add_stringvalue("Gemini API Key", gemini_key)
        self.anthropic_item = ai.add_stringvalue("Anthropic API Key", anthropic_key)
        
        from biscuit.common.ui import IconLabelButton, Icons
        IconLabelButton(ai, "Save Keys", Icons.SAVE, self.save_ai_keys).pack(fill=tk.X, pady=10)

    def save_clippy_settings(self, *_) -> None:
        try:
            self.base.config.clippy_enabled = self.clippy_enabled_item.value
            self.base.config.clippy_listeners = [
                l for l, item in self.clippy_listeners_items.items() if item.value
            ]
            self.base.config.save_config()
            
            # Restart or stop context engine
            if self.base.context_engine:
                self.base.context_engine.stop()
                if self.base.config.clippy_enabled:
                    self.base.context_engine.setup() # Re-initialize watchers based on new listeners
                    self.base.context_engine.start()
            
            # Update Clippy UI visibility
            if self.base.clippy:
                if self.base.config.clippy_enabled:
                    self.base.clippy.deiconify()
                else:
                    self.base.clippy.withdraw()
            
            # Update Statusbar Icon
            if hasattr(self.base.statusbar, 'clippy_toggle'):
                if self.base.config.clippy_enabled:
                    self.base.statusbar.clippy_toggle.show()
                else:
                    self.base.statusbar.clippy_toggle.hide()

            self.base.notifications.info("Clippy settings applied successfully!")
        except Exception as e:
            self.base.notifications.error(f"Failed to apply Clippy settings: {e}")

    def save_ai_keys(self, *_) -> None:
        import os
        import toml
        
        secrets_path = os.path.join(self.base.datadir, "secrets.toml")
        try:
            secrets = {
                "GEMINI_API_KEY": self.gemini_item.value,
                "ANTHROPIC_API_KEY": self.anthropic_item.value
            }
            with open(secrets_path, "w") as f:
                toml.dump(secrets, f)
            
            # Refresh AI view if active
            if hasattr(self.base, 'ai') and self.base.ai:
                agent_view = self.base.ai
                agent_view.api_keys["gemini"] = secrets["GEMINI_API_KEY"]
                agent_view.api_keys["anthropic"] = secrets["ANTHROPIC_API_KEY"]
                agent_view.add_chat()
                
            self.base.notifications.info("AI Keys saved successfully!")
        except Exception as e:
            self.base.notifications.error(f"Failed to save secrets: {e}")

    def add_section(self, name: str) -> Section:
        """Add a section to the settings editor

        Args:
            name (str): name of the section

        Returns:
            Section: section to add items to"""

        section = Section(self.container.content, name)
        section.pack(fill=tk.X, expand=True, pady=10)
        self.sections.append(section)

        shortcut = Button(self.tree, name)
        shortcut.pack(fill=tk.X)
        shortcut.config()

        return section

    def show_result(self, items):
        """Show the search results in the settings editor

        Args:
            items (list): list of items to show in the settings editor"""

        if not any(items):
            return self.show_no_results()

    def show_no_results(self):
        """Show no results found message in the settings editor"""
        ...
