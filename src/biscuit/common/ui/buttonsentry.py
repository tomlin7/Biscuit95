import tkinter as tk
from tkinter import ttk
from typing import Optional

from hintedtext import HintedEntry

from biscuit.common.icons import Icons
from biscuit.common.ui.icon import IconButton
from biscuit.common.ui.native import Frame


class ButtonsEntry(Frame):
    """Entry containing icon buttons on the right"""

    def __init__(
        self,
        master,
        hint: str,
        buttons: list[tuple[Icons, callable, Optional[str]]] = [],
        textvariable=None,
        *args,
        **kwargs):
        super().__init__(master) # , *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.entry = HintedEntry(
            self, hint=hint, textvariable=textvariable
        ) # removed font
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)

        self.actions = Frame(self)
        self.actions.grid(row=0, column=1, sticky=tk.NSEW)

        self.column = 0
        self.add_buttons(buttons)

    def add_button(self, icon: Icons, event=lambda _: None, icon2: str = None):
        b = IconButton(self.actions, icon, event, icon2)
        b.grid(row=0, column=self.column, sticky="")
        self.column += 1

    def add_buttons(self, buttons):
        for btn in buttons:
            self.add_button(*btn)

    def get(self, *args):
        return self.entry.get(*args)

    def clear(self):
        return self.entry.delete(0, tk.END)

    def delete(self, *args):
        return self.entry.delete(*args)

    def insert(self, *args):
        return self.entry.insert(*args)
