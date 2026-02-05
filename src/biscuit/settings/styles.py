from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk
from tkinter.font import Font

if typing.TYPE_CHECKING:
    from .settings import Settings


class Style(ttk.Style):
    """Handles the global styling of the app using clam theme"""

    def __init__(self, settings: Settings, *args, **kwargs) -> None:
        super().__init__(settings.base, *args, **kwargs)
        self.settings = settings
        self.base = settings.base

        # Use the clam theme as requested
        self.theme_use("clam")

        # Global TTK Configurations
        self.configure(".", font=self.settings.uifont)
        
        # Configure standard widgets with consistent padding/margins and borders
        self.configure("TFrame") 
        self.configure("TLabel", font=self.settings.uifont, padding=2)
        self.configure("TButton", font=self.settings.uifont, padding=(5, 2), borderwidth=1, relief="raised")
        self.configure("TCheckbutton", font=self.settings.uifont, padding=2)
        self.configure("TEntry", font=self.settings.uifont, padding=5, borderwidth=1, relief="sunken")
        self.configure("TMenubutton", font=self.settings.uifont, padding=(10, 5))
        self.configure("TNotebook", font=self.settings.uifont, borderwidth=0)
        self.configure("TNotebook.Tab", font=self.settings.uifont, padding=(10, 3), borderwidth=1, relief="raised")
        self.map("TNotebook.Tab",
                relief=[("selected", "sunken"), ("!selected", "raised")])
        
        # Configure PanedWindow sash
        self.configure("TPanedwindow", sashwidth=4, sashrelief="raised", background="#d0d0d0")
        
        # Activity Bar icons (font-based)
        self.configure("ActivityBar.TButton", font=("codicon", 11), width=0, padding=(5, 5), relief="flat", borderwidth=0)
        
        # Generic Icon Button
        self.configure("IconButton.TButton", font=("codicon", 12), width=0, padding=2)

        # Status Bar Styles
        self.configure("StatusBar.TFrame", padding=3, borderwidth=1, relief="raised")
        self.configure("StatusBar.Button.TFrame", padding=0, borderwidth=0, relief="flat")
        self.configure("StatusBar.TLabel", padding=(2, 0), font=("Segoe UI", 9))
        self.configure("StatusBar.Icon.TLabel", padding=(2, 0), font=("codicon", 10))

        # Menubar Styles
        self.configure("MenuBar.TFrame", padding=3, borderwidth=1, relief="raised")
        self.configure("MenubarItem.TButton", 
                      font=self.settings.uifont, 
                      padding=(1,1), 
                      relief="flat", 
                      borderwidth=1)
        self.map("MenubarItem.TButton",
                relief=[("active", "raised"), ("pressed", "sunken")])
        
        # Icon Button (used for window controls, notifications)
        self.configure("IconButton.TButton", font=("codicon", 12), width=0, padding=(8, 3), relief="flat", borderwidth=0)
        
        # SearchBar Style
        self.configure("SearchBar.TFrame", borderwidth=1, relief="sunken")
        
        # MenuItem Style (for dropdown menu items)
        self.configure("MenuItem.TButton", 
                      font=self.settings.uifont, 
                      padding=(10, 2), 
                      relief="flat",
                      anchor="w",
                      borderwidth=0)
        self.map("MenuItem.TButton",
                relief=[("active", "flat")])
        
        # Menu Container Style
        self.configure("Menu.TFrame", borderwidth=1, relief="raised", padding=2)
        
        # MenuItem Checkbutton Style (for checkable menu items)
        self.configure("MenuItem.TCheckbutton",
                      font=self.settings.uifont,
                      padding=(10, 2),
                      borderwidth=0)
        
        # Editor Tab Style
        self.configure("EditorTab.TFrame", borderwidth=1, relief="flat", padding=(3, 1))
        
        self.gen_fileicons()
        self.config_treeview()
        self.config_scrollbars()

    def config_treeview(self) -> None:
        self.monofont = Font(family=self.settings.config.font[0], size=10)

        # Trust theme for colors, only set professional rowheight
        self.configure("Treeview", font=self.settings.uifont, rowheight=25)
        self.configure("mono.Treeview", font=self.monofont, rowheight=25)
        self.configure("secondary.Treeview", font=self.monofont, rowheight=25)


    def config_scrollbars(self) -> None:
        """Configure scrollbar styles using default theme colors"""
        # Removed custom layouts to trust the native clam look (with arrows)
        pass

    def gen_fileicons(self) -> None:
        self.document_icn = tk.PhotoImage(
            "document",
            data="""
        iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAJ2AAACdgBx6C5rQA
        AABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADlSURBVDiNpZGxTgJBFEXPW9aGCRTYWht+wyVEEuq1md
        7Exm/A2NjxFUvBD1CQ7JZWlOhXQCNsoYnPajZk3Zks4VaTmfvOO8nAhRF3SJfa2X2XLwi39ZIi74XtzoOA0eIwUZVVQ+cDu
        AHmuTWz+mNUbdGo57HcKiTAc5KVb15AKIU1G4Ux6GMd0grgICIyBX26yw737j5uMZsm2VEBVBUAIeqfbeDLP4PcGmkqujgb
        LyDJjsuLDAJJWwFyax6ainV1L8BX9KX6BZHfr7ZDp93KYBCb9f6nfFUYhoZV+by+MutzLIP5A16TRi/mS3m5AAAAAElFTkS
        uQmCC
        """,
        )

        self.folder_icn = tk.PhotoImage(
            "foldericon",
            data="""
        iVBORw0KGgoAAAANSUhEUgAAABAAAAAMCAYAAABr5z2BAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB
        3d3cuaW5rc2NhcGUub3Jnm+48GgAAAJBJREFUKJHdzTEKwkAUhOF/loCFRbAVr+IhLAWLCPaW3sFGPIOm1Bt4hxSSEwRs7Z
        UdayErmnROO++bp93htJK0BUa8pxEq1ovZhQ/R/ni+G/LWEjW2y4Stx4NnmUU7l9R6YTxBbFLfb49sGlL4m9ieh84aAA17D
        sCfDLiHdwDqrlpwDTHGAqiA+IONQIW0fAFkySdEGFdeCgAAAABJRU5ErkJggg==""",
        )
