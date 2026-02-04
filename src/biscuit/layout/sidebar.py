from __future__ import annotations

import tkinter as tk
import typing
from tkinter import ttk

from biscuit.common.ui import Frame
from biscuit.common.ui.icon import Icons
from biscuit.views import *

if typing.TYPE_CHECKING:
    from biscuit.layout.statusbar.activitybar import ActivityBar


class SideBar(Frame):
    """Side bar - Contains and manages SidebarViews."""

    def __init__(
        self, master: Frame, activitybar: ActivityBar, *args, **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.views = []
        self.active_view = None
        self.visible = False

        self.activitybar = activitybar
        self.activitybar.attach_sidebar(self)

        self.default_views = {
            "Explorer": Explorer(self),
            # "Source Control": SourceControl(self),
            "Outline": Outline(self),
        }
        self.add_views(self.default_views.values())
        self.activitybar.add_separator()

        self.activitybar.add_button(
            Icons.SEARCH, "Search", lambda: self.base.editorsmanager.add_search()
        )
        self.activitybar.add_button(
            Icons.CHECK, "Problems", lambda: self.base.panel.show_problems()
        )

    def toggle(self) -> None:
        if self.visible:
            self.hide()
        else:
            if not self.active_view:
                self.show_explorer()
            else:
                self.pack()

    def add_views(self, views: list[SideBarView]) -> None:
        for view in views:
            self.add_view(view)

    def add_view(self, view: SideBarView) -> None:
        self.views.append(view)
        self.activitybar.add_view(view)

    def create_view(self, name: str, icon: str = "browser") -> SideBarView:
        view = SideBarView(self, name, icon)
        self.add_view(view)
        return view

    def delete_all_views(self) -> None:
        for view in self.views:
            view.destroy()
        self.views.clear()

    def delete_view(self, view: SideBarView) -> None:
        view.destroy()
        self.views.remove(view)

    @property
    def explorer(self) -> Explorer:
        return self.default_views["Explorer"]

    @property
    def source_control(self) -> SourceControl:
        return self.default_views["Source Control"]

    @property
    def outline(self) -> Outline:
        return self.default_views["Outline"]

    def show_view(self, view: SideBarView) -> SideBarView:
        for i in self.activitybar.buttons:
            if i.view == view:
                self.activitybar.set_active_slot(i)
                i.enable()
                self.active_view = view
                return view

    def show_explorer(self, *_) -> Explorer:
        return self.show_view(self.explorer)

    def show_source_control(self, *_) -> SourceControl:
        return self.show_view(self.source_control)

    def show_outline(self, *_) -> Outline:
        return self.show_view(self.outline)

    def pack(self, *args, **kwargs):
        if isinstance(self.master, ttk.PanedWindow):
            self.master.add(self, weight=0)
            # ttk.PanedWindow doesn't support minsize or width directly
        elif isinstance(self.master, tk.PanedWindow):
            try:
                self.master.add(
                    self, before=self.base.contentpane, width=270, stretch="never"
                )
            except:
                self.master.add(self, width=270, stretch="never")
            self.master.paneconfigure(self, minsize=50)
        else:
            super().pack(
                side=tk.LEFT, fill=tk.Y, before=self.base.contentpane, *args, **kwargs
            )
        self.visible = True

    def hide(self):
        if isinstance(self.master, tk.PanedWindow):
            self.master.forget(self)
        else:
            super().pack_forget()
        self.visible = False
