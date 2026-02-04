import tkinter as tk
from tkinter import ttk

from biscuit.common.ui.native import Frame, Label


class KeyB(Frame):
    """Visual representation of a key binding."""

    def __init__(self, master, key: str, *args, **kwargs) -> None:
        super().__init__(master) # , *args, **kwargs)
        self.key = key

        self.label = Label(
            self,
            text=key) # removed font
        self.label.pack(side=tk.LEFT) # removed padx/pady


class Shortcut(Frame):
    """Visual representation of a shortcut key combination."""

    def __init__(self, master, keys: tuple[str], *args, **kwargs) -> None:
        super().__init__(master) # , *args, **kwargs)
        self._keys = keys

        self.labels = []
        self.render()

    def render(self) -> None:
        for key in self._keys:
            self.add_key(key)

    def add_key(self, key: str) -> None:
        l = KeyB(self, key)
        l.pack(padx=5, side=tk.LEFT)
        self.labels.append(l)
