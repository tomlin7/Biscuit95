from __future__ import annotations

import tkinter as tk
import typing

from tkinterweb import HtmlFrame

from biscuit.common.ui import Frame, Scrollbar

if typing.TYPE_CHECKING:
    from ..text import TextEditor


class HTMLRenderer(Frame):
    def __init__(self, master, editor: TextEditor, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.editor = editor
        self.config()

        self.text = HtmlFrame(self, messages_enabled=False, vertical_scrollbar=False)
        self.scrollbar = Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=3, sticky=tk.NS)

    def refresh(self, *_):
        htmlcontent = self.editor.text.get_all_text()
        if "<title>" in htmlcontent and "</title>" not in htmlcontent:
            return

        self.text.load_html(htmlcontent)
        class t:
            border = "#d9d9d9"
            secondary_background = "#f0f0f0"
            secondary_foreground = "#000000"
            secondary_foreground_highlight = "#000000"
            primary_background = "#d9d9d9"
            primary_foreground = "#000000"
            primary_foreground_highlight = "#000000"
            biscuit = "#0078d7"
            biscuit_dark = "#005a9e"

        self.text.add_css(
            f"""
            CODE, PRE {{
                font-family: {self.base.settings.font['family']};
                font-size: {self.base.settings.font['size']}pt;
                background-color: {t.border};
                padding: 2px;
            }}
            BODY {{
                background-color: {t.secondary_background};
                color: {t.secondary_foreground};
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}

            hr {{
                border: 0;
                border-top: 1px solid {t.border};
                max-width: 100%;
            }}
            li{{
                margin-left:1px;
            }}
            :link    {{ color: {t.biscuit}; }}
            :visited {{ color: {t.biscuit_dark}; }}
            INPUT, TEXTAREA, SELECT, BUTTON {{ 
                background-color: {t.secondary_background};
                color: {t.secondary_foreground_highlight};
            }}
            INPUT[type="submit"],INPUT[type="button"], INPUT[type="reset"], BUTTON {{
                background-color: {t.primary_background};
                color: {t.primary_foreground};
                color: tcl(::tkhtml::if_disabled {t.primary_background}{t.primary_foreground_highlight});
            }}
            """
        )
