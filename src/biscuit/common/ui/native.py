import tkinter as tk
import typing
from tkinter import ttk

if typing.TYPE_CHECKING:
    from biscuit import App


class Text(tk.Text):
    """Text widget with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class Toplevel(tk.Toplevel):
    """Custom Toplevel widget for the app."""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class Canvas(tk.Canvas):
    """Canvas with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class Menubutton(ttk.Menubutton):
    """Menubutton with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class Label(ttk.Label):
    """Label with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None

    def set_text(self, text: str) -> None:
        self.config(text=text)


class Frame(ttk.Frame):
    """Frame with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class PanedWindow(ttk.PanedWindow):
    """PanedWindow with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None


class tkPanedWindow(tk.PanedWindow):
    """tk.PanedWindow with reference to base"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base: App = self._find_base(master)

    def _find_base(self, master):
        if hasattr(master, "base"):
            return master.base
        if hasattr(master, "master") and master.master:
            return self._find_base(master.master)
        return None
