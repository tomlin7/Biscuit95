import tkinter as tk
from tkinter import ttk

from biscuit.common.icons import Icons
from biscuit.common.ui.labels import Label
from biscuit.common.ui.native import Frame


class Icon(Label):
    """Simple label using codicons"""

    def __init__(
        self, master, icon: Icons = "", iconsize: int = 12, *args, **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.config(font=("codicon", iconsize))
        self.set_icon(icon)

    def set_icon(self, icon: str) -> None:
        self.config(text=icon)

    def set_color(self, color: str) -> None:
        pass


class IconButton(ttk.Button):
    """Icon button using codicons"""

    def __init__(
        self,
        master,
        icon: Icons,
        event=lambda *_: ...,
        icon2: Icons = "",
        iconsize=12,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, style="IconButton.TButton", *args, **kwargs)
        self.icons = [icon, icon2]
        self.icon2 = icon2
        self.switch = False

        self.event = event
        self.config(text=icon)

        self.bind("<Button-1>", self.onclick)

    def set_callback(self, event) -> None:
        self.event = event

    def onclick(self, *args) -> None:
        try:
            try:
                self.event(*args)
            except:
                self.event()

            self.v_onclick()
            self.toggle_icon()
        except Exception as e:
            print(e)

    def v_onclick(self) -> None: ...

    def set_icon(self, icon) -> None:
        self.config(text=icon)

    def toggle_icon(self) -> None:
        if not self.icon2:
            return

        self.switch = not self.switch
        self.config(text=self.icons[self.switch])

    def reset_icon(self) -> None:
        self.switch = False
        self.config(text=self.icons[self.switch])


class BorderedIconButton(Frame):
    """Icon button with a border"""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master)

        self.btn = IconButton(self, *args, **kwargs)
        self.btn.pack(fill="both", expand=True)

    def set_callback(self, event) -> None:
        self.btn.set_callback(event)

    def onclick(self, *args) -> None:
        self.btn.onclick(*args)

    def set_icon(self, icon) -> None:
        self.btn.set_icon(icon)

    def toggle_icon(self) -> None:
        self.btn.toggle_icon()

    def reset_icon(self) -> None:
        self.btn.reset_icon()
