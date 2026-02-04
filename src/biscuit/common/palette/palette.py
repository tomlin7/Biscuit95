from __future__ import annotations

import platform
import tkinter as tk
import typing
from tkinter import ttk

from ..actionset import ActionSet
from ..ui import Frame, Scrollbar, Toplevel
from ..ui.native import Canvas
from .item import PaletteItem
from .searchbar import SearchBar

if typing.TYPE_CHECKING:
    from biscuit import App


class Palette(Toplevel):
    """Palette - action menu centered horizontally and aligned to top of root."""

    def __init__(self, master: App, width=80, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.width = round(width * self.base.scale)
        self.active = False
        self.withdraw()

        if platform.system() == "Windows":
            from ctypes import byref, c_int, sizeof, windll

            GWL_STYLE = -16
            WS_CAPTION = 0x00C00000

            self.update_idletasks()
            hwnd = windll.user32.GetParent(self.winfo_id())

            style = windll.user32.GetWindowLongPtrW(hwnd, GWL_STYLE)
            style &= ~WS_CAPTION
            windll.user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style)

            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                dark_mode = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    byref(dark_mode),
                    sizeof(dark_mode))
            except:
                pass

            windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)
        else:
            self.overrideredirect(True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.row = 1
        self.selected = 0

        self.shown_items = []
        self.actionsets = []
        self.active_set = None
        self.active_items = None

        self.searchbar = SearchBar(self)
        self.searchbar.grid(row=0, sticky=tk.EW, padx=5, pady=(5, 2))

        self.items_container = Frame(self)
        self.items_container.grid(row=1, sticky=tk.NSEW, padx=2, pady=2)
        self.items_container.grid_columnconfigure(0, weight=1)
        self.items_container.grid_rowconfigure(0, weight=1)

        self.canvas = Canvas(self.items_container, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        self.scrollbar = Scrollbar(
            self.items_container, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.items_frame = Frame(self.canvas)
        self.items_window = self.canvas.create_window(
            (0, 0), window=self.items_frame, anchor=tk.NW
        )

        self.items_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.items_window, width=e.width))

        self.configure_bindings()

    def register_actionset(self, actionset_ref: ActionSet) -> None:
        self.actionsets.append(actionset_ref)

    def generate_help_actionset(self) -> None:
        self.help_actionset = ActionSet("Help", "?")
        for i in self.actionsets:
            i = i()
            if i.prefix:
                self.help_actionset.append(
                    (
                        i.prefix,
                        lambda _, i=i: self.after(50, self.show, i.prefix),
                        i.description)
                )

        self.register_actionset(lambda: self.help_actionset)

    def add_item(self, text: str, command, *args, **kwargs) -> PaletteItem:
        new_item = PaletteItem(self.items_frame, self, text, command, *args, **kwargs)
        new_item.pack(fill=tk.X)
        self.shown_items.append(new_item)
        return new_item

    def configure_bindings(self) -> None:
        self.bind("<FocusOut>", self.hide)
        self.bind("<Escape>", self.hide)
        self.refresh_selected()

    def on_mousewheel(self, event) -> str:
        if not self.active_items:
            return "break"

        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def pick_actionset(self, actionset: ActionSet) -> None:
        self.active_set = actionset

    def pick_file_search(self, term: str) -> None:
        self.active_set = self.base.explorer.get_actionset(term)

    def choose(self, *_) -> None:
        if item := self.shown_items[self.selected]:
            picked_command = item.command
            term = self.searchbar.term

            self.hide()
            picked_command(term)

    def get_items(self) -> ActionSet:
        return self.active_set

    def hide(self, *args) -> None:
        self.withdraw()
        self.reset()
        self.unbind_all("<MouseWheel>")

    def hide_all_items(self) -> None:
        for i in self.shown_items:
            i.destroy()
        self.shown_items = []
        self.canvas.yview_moveto(0)

    def reset_selection(self) -> None:
        self.selected = 0
        self.refresh_selected()

    def refresh_selected(self) -> None:
        if not self.shown_items:
            return

        for i in self.shown_items:
            i.deselect()

        try:
            item = self.shown_items[self.selected]
            item.select()
            self.after(10, self.ensure_visible, item)
        except IndexError as e:
            self.base.logger.error(f"Item '{self.selected}' doesnt exist: {e}")

    def ensure_visible(self, item):
        if not item.winfo_exists():
            return

        try:
            self.update_idletasks()
            item_y = item.winfo_y()
            item_h = item.winfo_height()

            cw_h = self.canvas.winfo_height()
            cv_y = self.canvas.yview()[0] * self.items_frame.winfo_height()

            total_h = self.items_frame.winfo_reqheight()
            if total_h == 0:
                return

            if item_y < cv_y:
                self.canvas.yview_moveto(item_y / total_h)
            elif item_y + item_h > cv_y + cw_h:
                self.canvas.yview_moveto((item_y + item_h - cw_h) / total_h)
        except tk.TclError:
            pass

    def reset(self) -> None:
        self.searchbar.clear()
        self.reset_selection()

    def search_bar_enter(self, *_) -> str:
        self.choose()
        return "break"

    def show_no_results(self) -> None:
        self.hide_all_items()
        self.reset_selection()
        self.add_item("No results found", lambda _: ...)

    def select(self, delta: int) -> None:
        if not self.shown_items:
            return "break"

        self.selected += delta
        self.selected = min(max(0, self.selected), len(self.shown_items) - 1)
        self.refresh_selected()

    def show_items(self, items: list[PaletteItem]) -> None:
        self.hide_all_items()
        self.active_items = items

        for i in self.active_items:
            item = self.add_item(*i)
            item.mark_term(self.searchbar.term)

    def show(self, prefix: str = None, default: str = None) -> None:
        self.update_idletasks()
        self.update()
        width = 600
        height = 400

        x = self.master.winfo_rootx() + int((self.master.winfo_width() - width) / 2)
        y = self.master.winfo_rooty() + 100

        self.minsize(width, 0)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()

        self.focus_set()
        self.searchbar.focus()
        self.searchbar.add_prefix(prefix)

        if default:
            self.searchbar.set_search_term(default)

        self.bind_all("<MouseWheel>", self.on_mousewheel)
