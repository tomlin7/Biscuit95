from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import typing

from ..ui import Text

if typing.TYPE_CHECKING:
    from . import Palette


class PaletteItem(Text):
    """Palette Item - represents an action that can be performed by the user."""

    def __init__(
        self,
        master: tk.Frame | ttk.Frame,
        palette: Palette,
        text: str,
        command: str,
        description="",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.palette = palette
        self.text = text
        self.description = description
        self.command = command

        self.config(
            font=self.base.settings.uifont,
            cursor="hand2",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            highlightthickness=0,
            width=30,
            height=1,
            spacing1=2,
            spacing3=2,
        )

        self.tag_config("term", font=self.base.settings.uifont_bold)
        self.tag_config("description", font=self.base.settings.font)

        self.insert(tk.END, text)
        if description:
            self.insert(tk.END, f"   {description}", "description")
        self.config(state=tk.DISABLED)

        self.bind("<Button-1>", self.on_click)

        self.selected = False
        self.hovered = False

    def on_click(self, *args) -> None:
        term = self.palette.searchbar.term
        self.palette.hide()
        self.command(term)

    def toggle_selection(self) -> None:
        if self.selected:
            self.select()
        else:
            self.deselect()

    def mark_term(self, term: str) -> None:
        start_pos = self.text.lower().find(term.lower())
        end_pos = start_pos + len(term)
        self.tag_remove("term", 1.0, tk.END)
        self.tag_add("term", f"1.{start_pos}", f"1.{end_pos}")

    def select(self) -> None:
        self.selected = True

    def deselect(self) -> None:
        self.selected = False
