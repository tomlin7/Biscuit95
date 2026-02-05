import tkinter as tk
from tkinter import ttk

from biscuit.common.icons import Icons


class Checkable(ttk.Checkbutton):
    """A checkable menu item
    Inherits from ttk.Checkbutton"""

    def __init__(
        self, master, text, command=lambda *_: ..., checked=False, *args, **kwargs
    ) -> None:
        """Create a checkable menu item

        Args:
            master: The parent widget
            text: The text to display on the menu item
            command: The command to run when the item is clicked
            checked: The initial checked state
            *args: Additional arguments to pass to the Checkbutton
        """
        
        self.var = tk.BooleanVar(value=checked)
        self.command = command
        self.menu = master.master
        
        super().__init__(
            master,
            text=text,
            variable=self.var,
            style="MenuItem.TCheckbutton",
            command=self.on_click,
            *args,
            **kwargs,
        )

    def on_click(self, *_) -> None:
        self.menu.event_chosen()
        self.command()
