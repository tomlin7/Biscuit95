from __future__ import annotations

import tkinter as tk
import typing

from biscuit.common.ui import Frame
from biscuit.views import *

from .panelbar import PanelBar

if typing.TYPE_CHECKING:
    from ..content import Content


class Panel(Frame):
    """Panel - container for panel views with a panelbar."""

    def __init__(self, master: Content, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master: Content = master

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(height=300)

        self.panelbar = PanelBar(self)
        self.panelbar.grid(row=0, column=0, sticky=tk.EW)

        self.views: list[PanelView] = []

        self.default_views = [Problems(self), Logs(self), Inspect(self), Terminal(self)]
        self.add_views(self.default_views)

    def add_views(self, views: list[PanelView]) -> None:
        for view in views:
            self.add_view(view)

    def add_view(self, view: PanelView) -> None:
        self.views.append(view)
        view.generate_actions(self.panelbar)
        self.panelbar.add_tab(view)

    def delete_all_views(self) -> None:
        for view in self.views:
            view.destroy()
        self.views.clear()

    def delete_view(self, view: PanelView) -> None:
        view.destroy()
        self.views.remove(view)

    def set_active_view(self, view: PanelView) -> None:
        for tab in self.panelbar.active_tabs:
            if tab.view == view:
                self.panelbar.set_active_tab(tab)
                tab.select()

    @property
    def problems(self) -> Problems:
        return self.default_views[0]

    @property
    def logger(self) -> Logs:
        return self.default_views[1]

    @property
    def control(self) -> Inspect:
        return self.default_views[2]

    @property
    def terminals(self) -> Terminal:
        return self.default_views[3]

    def show_terminal(self, *_) -> None:
        if not self.terminals.active_terminal:
            self.terminals.add_default_terminal()
        self.set_active_view(self.terminals)
        self.show_panel()

    def show_problems(self, *_) -> None:
        self.set_active_view(self.problems)
        self.show_panel()

    def show_logs(self, *_) -> None:
        self.set_active_view(self.logger)
        self.show_panel()

    def toggle_panel(self, *_) -> None:
        self.base.contentpane.toggle_panel()

    def switch_to_terminal(self, *_) -> None:
        if not self.terminals.active_terminal:
            self.terminals.add_default_terminal()
        self.set_active_view(self.terminals)

    def show_panel(self) -> None:
        self.base.contentpane.show_panel()
