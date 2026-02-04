from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk

from biscuit.common.ui import Frame, tkPanedWindow

from .editors import EditorsManager
from .panel import Panel

if typing.TYPE_CHECKING:
    ...


class Content(Frame):
    """Content Pane

    - Contains the EditorsPane and Panel
    - Manages the visibility of the Panel and the EditorPane
    """

    def __init__(self, master: Frame, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.base.contentpane = self

        self.container = tkPanedWindow(self, orient=tk.VERTICAL, bd=0, sashwidth=2)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.editorspane = EditorsManager(self.container)
        self.panel = Panel(self.container)
        self._panel_enabled = False
        self._panel_maxed = False

        self.container.add(self.editorspane, stretch="always")

    def show_panel(self) -> None:
        if not self._panel_enabled:
            self.toggle_panel()

    def toggle_panel(self, *_) -> None:
        if self._panel_enabled:
            self.container.forget(self.panel)
        else:
            if self._panel_maxed:
                self.container.forget(self.editorspane)
                self.container.add(self.panel, stretch="always")
            else:
                self.container.add(self.panel, height=300, stretch="never")

            if not self.panel.terminals.active_terminal:
                self.panel.terminals.open_terminal()

        self._panel_enabled = not self._panel_enabled

    def toggle_max_panel(self, *_) -> None:
        if self._panel_maxed:
            self.container.forget(self.panel)
            self.container.add(self.editorspane, stretch="always")
            self.container.add(self.panel, height=300, stretch="never")
        else:
            self.container.forget(self.editorspane)
            self.container.add(self.panel, stretch="always")

        self._panel_maxed = not self._panel_maxed

    def pack(self, *args, **kwargs):
        if isinstance(self.master, ttk.PanedWindow):
            self.master.add(self, weight=1)
            # ttk.PanedWindow doesn't support minsize configuration
        elif isinstance(self.master, tk.PanedWindow):
            self.master.add(self, stretch="always")
            self.master.paneconfigure(self, minsize=100)
        else:
            super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, *args, **kwargs)
