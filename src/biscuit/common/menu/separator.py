import tkinter as tk


class Separator(tk.Label):
    """A separator for the menu"""

    def __init__(self, master, length=20, *args, **kwargs) -> None:
        """Create a separator

        Args:
            master: The parent widget
            length: The length of the separator
        """

        super().__init__(master, *args, **kwargs)
        self.base = getattr(master, "base", None)
        self.master = master

        if self.base:
            self.config(text="—" * round((length * self.base.scale)))
        else:
            self.config(text="—" * length)
        # pady=0,
        # height=1)
