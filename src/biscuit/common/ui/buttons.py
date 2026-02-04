import tkinter as tk
from tkinter import ttk

from biscuit.common.icons import Icons
from biscuit.common.ui.native import Frame


class Button(ttk.Button):
    """A ttk style button"""

    def __init__(self, master, text, command=lambda: None, *args, **kwargs) -> None:
        super().__init__(master, text=text, command=command, *args, **kwargs)
        self.master = master
        self.base = master.base


class FlatButton(ttk.Button):
    """A flat style button (legacy compatibility)"""

    def __init__(self, master, text, command=lambda _: None, *args, **kwargs) -> None:
        super().__init__(master, text=text, command=command, *args, **kwargs)


class HoverChangeButton(ttk.Button):
    """A flat style button changing text on hover"""

    def __init__(
        self, master, text, command=lambda _: None, hovertext=None, *args, **kwargs
    ) -> None:
        super().__init__(master, text=text, command=command, *args, **kwargs)
        self.text = text
        self.hovertext = hovertext


class IconLabelButton(Frame):
    """Icon label button with both text and icon"""

    def __init__(
        self,
        master,
        text=None,
        icon: Icons = "",
        callback=lambda *_: None,
        iconside=tk.LEFT,
        expandicon=True,
        iconsize=14,
        icon_visible=True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self.text = text
        self.icon = icon
        self.icon_visible = icon_visible
        self.callback = callback
        self.codicon = self.icon

        if icon:
            self.icon_label = ttk.Label(
                self,
                text=self.codicon if self.icon_visible else "    ",
            )
            self.icon_label.pack(side=iconside, fill=tk.BOTH, expand=expandicon)

        if text:
            self.text_label = ttk.Label(
                self,
                text=self.text,
            )
            self.text_label.pack(side=iconside, fill=tk.BOTH, expand=True)

        self.config_bindings()
        self.visible = False

    def config_bindings(self) -> None:
        self.bind("<Button-1>", self.on_click)
        if hasattr(self, "text_label"):
            self.text_label.bind("<Button-1>", self.on_click)
        if hasattr(self, "icon_label"):
            self.icon_label.bind("<Button-1>", self.on_click)

    def on_click(self, *_) -> None:
        self.callback()

    def toggle_icon(self) -> None:
        try:
            self.icon_label.config(
                text=self.codicon if not self.icon_visible else "    "
            )
            self.icon_visible = not self.icon_visible
        except Exception:
            pass

    def change_text(self, text) -> None:
        try:
            self.text_label.config(text=text)
        except Exception:
            pass

    def change_icon(self, icon) -> None:
        try:
            self.icon_label.config(text=icon)
        except Exception:
            pass

    def set_pack_data(self, **kwargs) -> None:
        self.pack_data = kwargs

    def get_pack_data(self):
        return self.pack_data

    def show(self) -> None:
        if not self.visible:
            self.visible = True
            self.pack(**self.get_pack_data())

    def hide(self) -> None:
        if self.visible:
            self.visible = False
            self.pack_forget()
