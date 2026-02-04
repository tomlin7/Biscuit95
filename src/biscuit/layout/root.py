"""Layout

Contains the layout of the application. It is divided into 3 main parts:

Root
├── Menubar
├── <Container>
│  ├── Sidebar (Explorer, Search, Source Control, etc.)
│  └── Content
│     ├── Editors
│     └── Panel (Terminals, Logs, Problems, etc.)
└── StatusBar

The layout is designed to be modular and flexible. Each part can be easily replaced or modified.
Extensions can easily access and modify the layout.
"""

from __future__ import annotations

import tkinter as tk
import typing

from biscuit.common.ui import Frame, PanedWindow, tkPanedWindow
from biscuit.layout.statusbar import activitybar

from .content import *
from .menubar import Menubar
from .secondary_sidebar import SecondarySideBar
from .sidebar import SideBar
from .statusbar import Statusbar

if typing.TYPE_CHECKING:
    from ..app import App


class Root(Frame):
    """Root of the application

    - Contains the Menubar, Sidebar, Content Pane, and StatusBar
    - Manages the resizing of the application
    """

    def __init__(self, base: App, *args, **kwargs) -> None:
        super().__init__(base, *args, **kwargs)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.subcontainer = tkPanedWindow(
            self, orient=tk.HORIZONTAL, bd=0, sashwidth=2 #, bg=self.base.settings.style.theme.background
        )
        self.sidebar = SideBar(
            self.subcontainer, activitybar=self.statusbar.activitybar
        )
        self.content = Content(self.subcontainer)
        self.secondary_sidebar = SecondarySideBar(
            self.subcontainer, activitybar=self.statusbar.secondary_activitybar
        )

        self.menubar.pack(fill=tk.X)
        self.subcontainer.pack(fill=tk.BOTH, expand=True)
        self.statusbar.pack(fill=tk.X)

        self.content.pack()
        self.pack(fill=tk.BOTH, expand=True)

    def toggle_sidebar(self) -> None:
        self.sidebar.toggle()
