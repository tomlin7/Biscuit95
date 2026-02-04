from __future__ import annotations

import typing
from tkinter import ttk

from biscuit.common import Menu

if typing.TYPE_CHECKING:
    from . import Menubar


class MenubarItem(ttk.Button):
    def __init__(self, master: Menubar, text, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.name = text
        self.config(
            text=text,
        )
        # padx=10,
        # pady=5,
        # font=self.base.settings.uifont)

        self.menu = Menu(self, self.name)
        self.bind("<<Hide>>", self.deselect)
        self.bind("<Button-1>", self.onclick)
        self.bind("<Enter>", self.hover)

    def onclick(self, *_):
        self.menu.show()
        self.select()

    def hover(self, *_):
        self.master.switch_menu(self)

    def select(self):
        return
        self.config(bg=None)

    def deselect(self, *_):
        return
        self.config(bg=None)
