from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk

from biscuit.common import Icons
from biscuit.common.ui import Bubble

if typing.TYPE_CHECKING:
    from biscuit.views import SideBarView

    from .activitybar import ActivityBar


class SBubble(Bubble):
    def get_pos(self) -> str:
        return (
            f"+{int(self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) / 2)}"
            + f"+{self.master.winfo_rooty() - self.master.winfo_height() - 10}"
        )


class ActionButton(ttk.Button):
    """Action buttons for activity bar - used to switch between views in the sidebar."""

    def __init__(
        self,
        master: ActivityBar,
        icon: str,
        name: str,
        callback: typing.Callable = None,
        view: SideBarView = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, style="ActivityBar.TButton", *args, **kwargs)
        self.master: ActivityBar = master

        self.view = view
        self.callback = callback
        self.enabled = False

        self.bubble = SBubble(self, text=name)
        self.bind("<Enter>", self.bubble.show)
        self.bind("<Leave>", self.bubble.hide)

        self.config(text=icon)
        # relief=tk.FLAT,
        # font=("codicon", 12),
        # cursor="hand2",
        # padx=5,
        # pady=5)
        # self.pack(fill=tk.X, side=tk.TOP)

        self.bind("<Button-1>", self.toggle)

    def toggle(self, *_) -> None:
        if self.callback:
            self.callback()
            self.bubble.hide()
            return

        if not self.enabled:
            self.master.set_active_slot(self)
            self.enable()
        else:
            self.disable()

        self.bubble.hide()

    def enable(self) -> None:
        if not self.enabled:
            self.master.sidebar.pack()
            self.view.grid(column=0, row=1, sticky=tk.NSEW)
            self.enabled = True

    def disable(self) -> None:
        if self.enabled:
            self.master.sidebar.hide()
            self.view.grid_remove()
            self.enabled = False
