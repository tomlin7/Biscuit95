from __future__ import annotations

import tkinter as tk
import typing

import mistune
from mistune import InlineParser
from mistune.plugins.abbr import abbr
from mistune.plugins.def_list import def_list
from mistune.plugins.footnotes import footnotes
from mistune.plugins.formatting import strikethrough
from mistune.plugins.speedup import speedup
from mistune.plugins.table import table
from mistune.plugins.task_lists import task_lists
from mistune.plugins.url import url
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from tkinterweb import HtmlFrame

from biscuit.common.ui import Frame, Scrollbar

if typing.TYPE_CHECKING:
    from ..text import TextEditor


class HighlightRenderer(mistune.HTMLRenderer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.formatter = html.HtmlFormatter(style="monokai")

    def block_code(self, code, info=None):
        try:
            if info:
                lexer = get_lexer_by_name(info, stripall=True)
                return highlight(code, lexer, self.formatter)
        except Exception as e:
            print(e)

        return "<pre><code>" + mistune.escape(code) + "</code></pre>"


class MDRenderer(Frame):
    def __init__(self, master, editor: TextEditor, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.editor = editor
        self.config()

        self.renderer = HighlightRenderer(escape=False)
        self.formatter = self.renderer.formatter
        self.markdown = mistune.Markdown(
            renderer=self.renderer,
            inline=InlineParser(),
            plugins=[
                abbr,
                def_list,
                footnotes,
                strikethrough,
                speedup,
                table,
                task_lists,
                url,
            ],
        )
        self.text = HtmlFrame(self, messages_enabled=False, vertical_scrollbar=False)
        self.scrollbar = Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=3, sticky=tk.NS)

        # Minimal CSS - no colors, just fonts and layout
        pygments_css = self.formatter.get_style_defs(".highlight")
        self.css = f"""
            {pygments_css}
            CODE, PRE {{
                font-family: {self.base.settings.font["family"]};
                font-size: {self.base.settings.font["size"]}pt;
                padding: 2px;
            }}
            BODY {{
                align-items: left;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            hr {{
                border: 0;
                border-top: 1px solid;
                max-width: 100%;
            }}
            li {{
                margin-left: 1px;
            }}
            tr, th, td {{
                border: 1px solid;
            }}
            """

    def refresh(self, *_):
        rawmd = self.editor.text.get_all_text()
        self.text.load_html(self.markdown(rawmd))
        self.text.add_css(self.css)
