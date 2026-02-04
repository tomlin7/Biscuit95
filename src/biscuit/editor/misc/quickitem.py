import os
import tkinter as tk
from typing import Callable, List

from biscuit.common.icons import Icons
from biscuit.common.ui import Icon, Shortcut
from biscuit.common.ui.native import Frame, Label


class RecentItem(Frame):
    """Recent Menu Item"""

    def __init__(self, master, path: str, callback: Callable, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.text = os.path.abspath(path)
        self.callback = callback

        self.bg = self.fg = self.hbg = self.hfg = None

        self.frame = Frame(self)
        self.frame.pack(pady=1, padx=1, expand=True, fill=tk.BOTH)

        self.frame2 = Frame(self.frame)  # , pady=2)
        self.frame2.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

        self.label = tk.Label(
            self.frame2,
            text=os.path.basename(path).upper(),
            font=("Consolas", 10, "bold"),
        )
        self.label.pack(side=tk.LEFT, padx=5)

        self.fullpath_label = Label(
            self.frame2,
            text=(
                "..." + os.path.abspath(path)[-25:]
                if len(os.path.abspath(path)) > 25
                else os.path.abspath(path)
            ),
        )
        self.fullpath_label.pack(side=tk.RIGHT, padx=5)

        self.frame2.bind("<Button-1>", self.callback)
        self.label.bind("<Button-1>", self.callback)
        self.fullpath_label.bind("<Button-1>", self.callback)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, *_) -> None:
        self.frame.config()
        self.label.config()
        self.fullpath_label.config()
        self.frame2.pack(fill=tk.BOTH, expand=True, pady=(0, 3))

    def on_leave(self, *_) -> None:
        self.frame.config()
        self.label.config()
        self.fullpath_label.config()
        self.frame2.pack(fill=tk.BOTH, expand=True, pady=(3, 0))


class QuickItem(Frame):
    """Quick Menu Item"""

    def __init__(
        self,
        master,
        text: str,
        icon: str,
        callback: Callable,
        shortcut: List[str],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.text = text
        self.icon = icon
        self.callback = callback
        self.shortcut = shortcut

        self.bg = self.fg = self.hbg = self.hfg = None

        self.icon = Icon(self, icon=icon)
        self.icon.pack(side=tk.LEFT, padx=5)

        self.label = Label(self, text=text)
        self.label.bind("<Button-1>", self.callback)
        self.label.pack(side=tk.LEFT, padx=5)

        self.shortcutlabel = Shortcut(self, shortcut)
        self.shortcutlabel.pack(side=tk.RIGHT, padx=5)
        self.shortcutlabel.bind("<Button-1>", self.callback)

        # self.config(padx=5, pady=5)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.callback)
        self.on_leave()

    def on_enter(self, *_) -> None:
        self.config()
        self.icon.config()
        self.label.config()
        self.shortcutlabel.config()

    def on_leave(self, *_) -> None:
        self.config()
        self.icon.config()
        self.label.config()
        self.shortcutlabel.config()
