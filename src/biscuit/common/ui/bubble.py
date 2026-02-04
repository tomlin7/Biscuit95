import tkinter as tk

from biscuit.common.ui.labels import Label
from biscuit.common.ui.native import Toplevel


class Bubble(Toplevel):
    """Hover bubble for showing information/tips on hover."""

    def __init__(self, master, text, *args, **kw) -> None:
        super().__init__(master) # , *args, **kw)
        self.overrideredirect(True)
        self.label = Label(
            self,
            text=text,
            # padx=5,
            # pady=5,
            # font=self.base.settings.uifont,
        )
        self.label.pack()
        self.withdraw()

    def get_pos(self, *_) -> str:
        return (
            f"+{self.master.winfo_rootx() + self.master.winfo_width() + 5}"
            + f"+{int(self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) / 2)}"
        )

    def change_text(self, text) -> None:
        self.label.config(text=text)

    def show(self, *_) -> None:
        self.update_idletasks()
        self.geometry(self.get_pos())
        self.deiconify()

    def hide(self, *_) -> None:
        self.withdraw()
