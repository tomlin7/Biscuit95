from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import typing

from biscuit.common.icons import Icons
from biscuit.common.ui import (
    Entry,
    Frame,
    Label,
    WebLinkLabel,
    WrappingLabel,
)

if typing.TYPE_CHECKING:
    ...


class AIPlaceholder(Frame):
    """Home page for the AI assistant view.

    Now supports both Google Gemini and Anthropic Claude."""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.config(padding=20)

        self.label = WrappingLabel(
            self,
            font=self.base.settings.uifont,
            justify=tk.LEFT,
            anchor=tk.W,
            text="AI features are disabled because no API keys were found.\n\nPlease configure your AI providers in Settings to start chatting.",
        )
        self.label.pack(fill=tk.X, pady=(0, 20))

        if self.base.commands.open_settings:
            btn = ttk.Button(
                self,
                text="Open Settings",
                command=self.base.commands.open_settings,
            )
            btn.pack(fill=tk.X, pady=5)
        
        self.link = WebLinkLabel(
            self, text="Get Gemini Key", link="https://aistudio.google.com/app/apikey"
        )
        self.link.pack(fill=tk.X, pady=(20, 0))

        self.link2 = WebLinkLabel(
            self,
            text="Get Anthropic Key",
            link="https://console.anthropic.com/settings/keys",
        )
        self.link2.pack(fill=tk.X)
