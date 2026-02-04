import tkinter as tk

from biscuit.common.icons import Icons
from biscuit.common.ui.icon import IconButton
from biscuit.common.ui.native import Frame


class Closable(Frame):
    """For implementing a list of closeable items."""

    def __init__(
        self,
        master,
        text=None,
        icon: Icons = "",
        callback=lambda *_: None,
        closefn=lambda *_: None,
        iconside=tk.LEFT,
        padx=1,
        pady=1,
        *args,
        **kwargs) -> None:
        super().__init__(master) # , padx=padx, pady=pady, *args, **kwargs)
        self.callback = callback
        self.closefn = closefn
        self.text = text
        self.icon = icon

        self.icon_label = None
        self.text_label = None

        if icon:
            self.icon_label = tk.ttk.Label(
                self,
                text=self.icon) # removed anchor/font
            self.icon_label.pack(side=iconside, fill=tk.BOTH) # removed padx

        if text:
            self.text_label = tk.ttk.Label(
                self,
                text=self.text) # removed anchor/font/pady
            self.text_label.pack(
                side=iconside, fill=tk.BOTH, expand=True
            ) # removed padx

        self.close_btn = IconButton(self, Icons.CLOSE, self.closefn)
        self.close_btn.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.config_bindings()
        self.visible = False

    def config_bindings(self) -> None:
        self.bind("<Button-1>", self.on_click)
        if self.text:
            self.text_label.bind("<Button-1>", self.on_click)
        if self.icon:
            self.icon_label.bind("<Button-1>", self.on_click)

    def on_click(self, *_) -> None:
        self.callback()

    def change_text(self, text) -> None:
        self.text_label.config(text=text)

    def change_icon(self, icon) -> None:
        self.icon_label.config(text=icon)

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
