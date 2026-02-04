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


class Renderer(Frame):
    """Renderer for the AI assistant chat view."""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
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
        self.htmlframe = HtmlFrame(
            self, messages_enabled=False, vertical_scrollbar=False, shrink=True
        )

        self.htmlframe.pack(fill=tk.BOTH, expand=True)

        self.header = "<html><head></head><body>"
        self.footer = "</body></html>"
        self.content = ""

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
                font-family: {self.base.settings.uifont["family"]};
                font-size: {self.base.settings.uifont["size"]}pt;
                margin: 0;
                padding: 0 5px;
                overflow-x: hidden;
                width: 100%;
                word-wrap: break-word;
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
                margin-left: 15px;
                padding-bottom: 4px;
            }}
            tr, th, td {{
                border: 1px solid;
            }}
            """

    def write(self, content: str, clear=False) -> None:
        if clear:
            self.content = self.markdown(content)
        else:
            self.content += self.markdown(content)

        full_html = f"{self.header}{self.content}{self.footer}"
        self.htmlframe.load_html(full_html)
        self.htmlframe.add_css(self.css)
