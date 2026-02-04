import tkinter as tk
from tkinter import ttk

from hintedtext import HintedEntry

from biscuit.common.ui.native import Frame


class Entry(Frame):
    def __init__(self, master, hint="", *args, **kwargs) -> None:
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.entry = HintedEntry(self, hint=hint) # removed font
        # self.entry.config(*args, **kwargs) # commented out per-component styling
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)
        self.entry.add_hint(hint)

    def insert(self, *args) -> None:
        self.entry.insert(*args)

    def get(self, *args) -> str:
        return self.entry.get(*args)

    def delete(self, *args) -> None:
        self.entry.delete(*args)

    def bind(self, *args, **kwargs) -> None:
        self.entry.bind(*args, **kwargs)
