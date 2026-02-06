from __future__ import annotations

import tkinter as tk
import typing

from pygments.lexers._mapping import LEXERS

from biscuit.common import ActionSet
from biscuit.common.icons import Icons
from biscuit.common.textutils import *
from biscuit.common.ui import Frame

from .activitybar import ActivityBar
from .button import SButton

if typing.TYPE_CHECKING:
    from biscuit.editor import Text


class Statusbar(Frame):
    """Status bar - displays information about the current file and editor state."""

    def __init__(self, master: Frame, *args, **kwargs) -> None:
        super().__init__(master, style="StatusBar.TFrame", *args, **kwargs)

        self.activitybar = ActivityBar(self)
        self.activitybar.pack(side=tk.LEFT, padx=(5, 0), pady=2)

        self.branch = self.add_button(
            text="main",
            icon=Icons.SOURCE_CONTROL,
            callback=self.base.commands.change_git_branch,
            description="Checkout branch",
            side=tk.LEFT,
            padx=(2, 0),
        )

        self.process_indicator = self.add_button(
            text="setting up environment",
            icon=Icons.SYNC,
            description="enabling language extensions",
            side=tk.LEFT,
            padx=(2, 0),
        )

        self.lc_actionset = self.create_actionset(
            "Goto line in active editor",
            ":",
            pinned=[["goto line: {}", self.goto_line]],
        )
        self.line_col_info = self.add_button(
            text="1,1",
            callback=self.base.commands.goto_line_column,
            description="Go to Line/Column",
            side=tk.RIGHT,
        )

        self.indent_actionset = self.create_actionset(
            "Change indentation",
            "indent:",
            [
                ("2 spaces", lambda e=None: self.base.set_tab_spaces(2)),
                ("4 spaces", lambda e=None: self.base.set_tab_spaces(4)),
                ("8 spaces", lambda e=None: self.base.set_tab_spaces(8)),
            ],
            pinned=[
                ["custom: {} spaces", self.change_custom_indentation],
            ],
        )
        self.indentation = self.add_button(
            text=f"{self.base.tab_spaces}sp",
            callback=self.base.commands.change_indentation_level,
            description="Change indentation",
            side=tk.RIGHT,
        )

        self.encoding_actionset = self.create_actionset(
            "Change file encoding",
            "encoding:",
            [("UTF-8", lambda e=None: print("encoding UTF-8", e))],
        )
        self.encoding = self.add_button(
            text="UTF-8",
            callback=self.base.commands.change_encoding,
            description="Change encoding",
            side=tk.RIGHT,
        )

        self.eol_actionset = self.create_actionset(
            "Change End of Line sequence",
            "eol:",
            [(i.upper(), self.change_eol(val)) for i, val in eol_map.items()],
        )
        self.eol = self.add_button(
            text="CRLF",
            callback=self.base.commands.change_end_of_line_character,
            description="Change End of Line sequence",
            side=tk.RIGHT,
        )

        items = [
            (aliases[0], self.change_language(aliases[0]))
            for _, _, aliases, _, _ in LEXERS.values()
            if aliases
        ]
        self.language_actionset = self.create_actionset(
            "Change Language Mode", "language:", items
        )
        self.file_type = self.add_button(
            text="Plain Text",
            callback=self.base.commands.change_language_mode,
            description="Change Language Mode",
            side=tk.RIGHT,
        )

        self.secondary_activitybar = ActivityBar(self)
        self.secondary_activitybar.pack(side=tk.RIGHT, padx=(0, 10))

        self.panel_toggle = SButton(
            self,
            icon=Icons.LAYOUT_PANEL_OFF,
            callback=self.toggle_panel,
            description="Toggle panel",
            icon2=Icons.LAYOUT_PANEL,
        )
        self.panel_toggle.set_pack_data(side=tk.RIGHT, padx=(0, 10))
        self.panel_toggle.show()
        
        self.clippy_toggle = SButton(
            self,
            icon=Icons.ROBOT,
            callback=self.toggle_clippy,
            description="Toggle Clippy",
        )
        self.clippy_toggle.set_pack_data(side=tk.RIGHT, padx=(0, 10))
        if self.base.config.clippy_enabled:
            self.clippy_toggle.show()

    def add_button(
        self,
        text="",
        icon="",
        callback: typing.Callable = None,
        description="",
        highlighted=False,
        **kwargs,
    ) -> SButton:
        btn = SButton(
            self, text=text, icon=icon, callback=callback, description=description
        )  # highlighted=highlighted)
        btn.set_pack_data(**kwargs)
        return btn

    def create_actionset(
        self, name: str, prefix: str, actions: list = [], pinned: list = []
    ) -> ActionSet:
        actionset = ActionSet(name, prefix, actions, pinned=pinned)
        self.base.palette.register_actionset(lambda: actionset)
        return actionset

    def toggle_sidebar(self) -> None:
        self.base.root.toggle_sidebar()

    def toggle_panel(self) -> None:
        self.base.toggle_terminal()

    def toggle_clippy(self) -> None:
        if self.base.clippy.winfo_viewable():
            self.base.clippy.close()
        else:
            self.base.clippy.user_closed = False
            self.base.clippy.deiconify()

    def toggle_editmode(self, state: bool) -> None:
        widgets = [
            self.file_type,
            self.indentation,
            self.line_col_info,
        ]
        for widget in widgets:
            widget.show() if state else widget.hide()

    def update_git_info(self) -> None:
        if self.base.git_found:
            self.branch.show()
            self.branch.change_text(f"{self.base.git.active_branch}")
        else:
            self.branch.hide()

    def on_open_file(self, text: Text) -> None:
        self.file_type.change_text(text.language)

    def set_line_col_info(self, line: int, col: int, selected: int = None) -> None:
        self.line_col_info.change_text(f"{line},{col} ")

    def set_encoding(self, encoding: str) -> None:
        self.encoding.change_text(text=encoding.upper())

    def set_spaces(self, spaces: int) -> None:
        self.indentation.change_text(text=f"{spaces}sp")

    def pack(self, **kwargs):
        super().pack(**kwargs)

    def goto_line(self, line: str) -> None:
        if line and line.isnumeric():
            self.base.editorsmanager.active_editor.content.goto_line(int(line))
        else:
            print("failed goto line", line)

    def change_custom_indentation(self, line: str = None) -> None:
        if line and line.strip().isnumeric():
            self.base.set_tab_spaces(int(line.strip()))
        else:
            print("failed change indentation", line)

    def change_eol(self, val: str) -> typing.Callable:
        return lambda _: self.base.editorsmanager.active_editor.content.text.change_eol(
            eol=val
        )

    def change_language(self, language: str) -> typing.Callable:
        return (
            lambda _: self.base.editorsmanager.active_editor.content.text.highlighter.change_language(
                language
            )
        )
