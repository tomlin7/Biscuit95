import tkinter as tk

from biscuit.common.ui import Frame

from .sidebar_item_toolbar import SideBarItemToolBar


class SideBarViewItem(Frame):
    """Container for the sidebar view items."""

    __actions__ = []
    title = "Item"

    def __init__(
        self, master, title: str = None, itembar=True, *args, **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)

        if title:
            self.title = title

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.enabled = True
        self.itembar_enabled = itembar

        if itembar:
            self.itembar = SideBarItemToolBar(self, self.title, self.__actions__)
            self.itembar.grid(row=0, column=0, sticky=tk.NSEW)

        self.content = Frame(self)
        self.content.master = self.master
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid(row=1 if itembar else 0, column=0, sticky=tk.NSEW)

    def add_action(self, icon: str, event) -> None:
        if self.itembar_enabled:
            self.itembar.add_action(icon, event)

    def set_title(self, title: str) -> None:
        if self.itembar_enabled:
            self.itembar.set_title(title)

    def toggle(self, *_) -> None:
        if not self.enabled:
            self.enable()
        else:
            self.disable()

    def enable(self) -> None:
        if not self.enabled:
            self.content.grid()
            self.enabled = True

    def disable(self) -> None:
        if self.enabled:
            self.content.grid_remove()
            self.enabled = False
