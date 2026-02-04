from __future__ import annotations

import webbrowser

from biscuit.common.ui.labels import WrappingLabel


class LinkLabel(WrappingLabel):
    """Label that acts as a link"""

    def __init__(
        self, master, text: str, command=lambda _: None, *args, **kwargs
    ) -> None:
        super().__init__(master, text=text)  # , *args, **kwargs)

        # self.config(
        #     # font=self.base.settings.uifont, # removed custom font
        #     cursor="hand2")
        self.set_command(command)

    def set_command(self, command) -> None:
        self.bind("<Button-1>", command)

    def pack(self, *args, **kwargs) -> LinkLabel:
        super().pack(*args, **kwargs)
        return self


class WebLinkLabel(LinkLabel):
    """LinkLabel that opens a web link"""

    def __init__(self, master, text, link=None, *args, **kwargs) -> None:
        super().__init__(master, text=text)  # , *args, **kwargs)
        self.link = link
        self.set_command(self.open_link)

    def open_link(self, *_) -> None:
        webbrowser.open(self.link)

    def set_link(self, link: str) -> None:
        self.link = link
        self.set_command(self.open_link)
