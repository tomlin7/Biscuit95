import tkinter as tk
from tkinter import ttk


class Separator(ttk.Separator):
    """A separator for the menu"""

    def __init__(self, master, length=20, *args, **kwargs) -> None:
        """Create a separator

        Args:
            master: The parent widget
            length: The length of the separator (ignored, kept for compatibility)
        """

        super().__init__(master, orient="horizontal", *args, **kwargs)
        self.base = getattr(master, "base", None)
        self.master = master
