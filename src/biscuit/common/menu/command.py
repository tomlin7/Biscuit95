from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk

if typing.TYPE_CHECKING:
    from .menu import Menu


class Command(ttk.Button):
    """A menu item

    Inherits from Menubutton"""

    def __init__(self, master, text, command=lambda *_: ..., *args, **kwargs) -> None:
        """Create a menu item

        Args:
            master: The parent widget
            text: The text to display on the menu item
            command: The command to run when the item is clicked
            *args: Additional arguments to pass to the Menubutton
        """

        super().__init__(master, style="MenuItem.TButton", *args, **kwargs)
        self.command = command
        self.menu = master.master

        self.config(
            text=text,
            width=0,
            command=self.on_click)
        self.bind("<Button-1>", self.on_click)

    def on_click(self, *_) -> None:
        self.menu.event_chosen()
        self.command()
