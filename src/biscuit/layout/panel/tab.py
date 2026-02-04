from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk

if typing.TYPE_CHECKING:
    from biscuit.views import PanelView

    from .panelbar import PanelBar


class Tab(ttk.Button):
    """Tab of panel bar - Panel views are attached to tabs."""

    def __init__(self, master: PanelBar, view: PanelView, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.view = view
        self.selected = False

        self.config(text=view.__class__.__name__)
        # padx=5,
        # pady=5,
        # font=self.base.settings.uifont)

        self.bind("<Button-1>", self.select)

    def deselect(self, *_) -> None:
        if self.selected:
            self.view.grid_remove()
            self.selected = False

    def select(self, *_) -> None:
        if not self.selected:
            self.master.set_active_tab(self)
            self.view.grid(column=0, row=1, sticky=tk.NSEW)
            self.selected = True
