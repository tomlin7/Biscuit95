from __future__ import annotations

import os
import tkinter as tk
import typing

from biscuit.common import Icons
from biscuit.common.ui import Frame, Icon, IconButton, Label

if typing.TYPE_CHECKING:
    from biscuit.editor import Editor

    from .editorsbar import EditorsBar


class Tab(Frame):
    """Editor Tab - shows filename, icon and close button."""

    def __init__(self, master: EditorsBar, editor: Editor, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master: EditorsBar = master
        self.editor = editor
        self.selected = False

        self.icon = Icon(self, Icons.FILE, iconsize=12)
        self.icon.pack(side=tk.LEFT, padx=5, fill=tk.Y)

        from tkinter import ttk
        
        self.name = ttk.Label(
            self,
            text=(
                f"{editor.filename} (working tree)" if editor.diff else editor.filename
            ),
            padding=(5, 0),
            font=self.base.settings.uifont)
        self.name.pack(side=tk.LEFT)

        self.closebtn = IconButton(
            self,
            Icons.CLOSE,
            iconsize=12,
            event=self.close)
        self.closebtn.pack(side=tk.RIGHT, fill=tk.Y)

        self.bind("<Button-1>", self.select)
        self.name.bind("<Button-1>", self.select)

    def close(self, *_) -> None:
        self.master.close_tab(self)

    def deselect(self, *_) -> None:
        if self.selected:
            self.editor.grid_remove()
            self.selected = False
            self.config(relief="flat", borderwidth=0)

    def select(self, *_) -> None:
        if not self.selected:
            self.master.set_active_tab(self)
            if self.base.active_directory and self.editor.filename:
                self.base.set_title(
                    f"{self.editor.filename} - {os.path.basename(self.base.active_directory)}"
                )
            elif self.editor.filename:
                self.base.set_title(self.editor.filename)
            self.editor.grid(column=0, row=1, sticky=tk.NSEW, in_=self.master.master)
            self.selected = True
            self.config(relief="raised", borderwidth=1)

        if (
            self.editor.path
            and self.editor.exists
            and self.editor.showpath
            and not self.editor.diff
        ):
            self.master.show_breadcrumbs()
            self.base.breadcrumbs.set_path(self.editor.path)
        else:
            self.master.hide_breadcrumbs()
